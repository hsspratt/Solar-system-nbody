"""Render the simulated orbits to a video file.

How it works
------------
1. ``solve_ivp`` uses an adaptive time step, so its output samples are NOT evenly spaced
   in time. Turning every n-th sample into a frame would make the bodies visibly speed up
   and slow down. The positions are therefore linearly interpolated onto an evenly spaced
   time grid with exactly ``n_frames`` points.
2. The figure is built once: one trail line and one marker per body, with the axis limits
   fixed from the whole trajectory so the camera does not jump between frames.
3. For every frame only the data of those existing artists is updated (``set_data_3d``),
   so each frame costs the same instead of re-plotting ever longer lines.
4. ``FuncAnimation.save`` draws each frame and streams its pixels straight into an
   FFmpeg process through a pipe, so memory use stays flat however long the video is.
   If FFmpeg is not installed the video is written as a GIF with Pillow instead. Pillow
   has no video encoder and keeps every frame in memory until the end, so the frame
   count and resolution are what bound its memory use.
"""

from pathlib import Path
import time
import warnings

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def resample_uniform(t, positions, n_frames):
    """Interpolate positions sampled at uneven times ``t`` onto ``n_frames`` even times.

    ``positions`` has shape (n_samples, n_bodies, 3); returns (t_frames, frames) where
    ``frames`` has shape (n_frames, n_bodies, 3).
    """
    t_frames = np.linspace(t[0], t[-1], n_frames)
    frames = np.empty((n_frames,) + positions.shape[1:])
    for body in range(positions.shape[1]):
        for axis in range(3):
            frames[:, body, axis] = np.interp(t_frames, t, positions[:, body, axis])
    return t_frames, frames


def pick_writer(out_path, fps, bitrate=4000):
    """Choose an encoder explicitly rather than relying on Matplotlib's silent fallback.

    Matplotlib's default writer is FFmpeg; when it is missing, ``save`` quietly swaps to
    Pillow, which buffers every frame in RAM and then cannot write ``.mp4`` at all.
    """
    out_path = Path(out_path)
    if animation.FFMpegWriter.isAvailable():
        # yuv420p is the pixel format every player (QuickTime, browsers) can decode
        writer = animation.FFMpegWriter(fps=fps, codec="libx264", bitrate=bitrate,
                                        extra_args=["-pix_fmt", "yuv420p"])
        return writer, out_path.with_suffix(".mp4")
    warnings.warn("FFmpeg was not found on PATH, so the animation is saved as a GIF with "
                  "Pillow. Install FFmpeg (e.g. `brew install ffmpeg`, `conda install "
                  "ffmpeg` or `sudo apt install ffmpeg`) for an MP4.")
    return animation.PillowWriter(fps=fps), out_path.with_suffix(".gif")


def render_orbit_animation(t, r_com_sol, names, out_path, colours=None, fps=30,
                           n_frames=300, size_px=960, dpi=120, title="Animated Orbit"):
    """Render the orbits in ``r_com_sol`` (shape (n_samples, 3*n_bodies)) to a video.

    Returns the path actually written (.mp4 with FFmpeg, .gif without).
    """
    n_bodies = len(names)
    positions = np.asarray(r_com_sol).reshape(len(t), n_bodies, 3)
    _, frames = resample_uniform(np.asarray(t), positions, n_frames)
    if colours is None:
        colours = plt.get_cmap("tab10").colors

    writer, out_path = pick_writer(out_path, fps)

    # H.264 with yuv420p needs even pixel dimensions, so size the figure in whole pixels.
    size_px -= size_px % 2
    fig = plt.figure(figsize=(size_px / dpi, size_px / dpi), dpi=dpi)
    ax = fig.add_subplot(projection="3d")
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Fixed, equal limits taken from the whole run so the view never rescales mid-video.
    centre = (frames.max(axis=(0, 1)) + frames.min(axis=(0, 1))) / 2
    half_range = (frames.max(axis=(0, 1)) - frames.min(axis=(0, 1))).max() / 2 * 1.05
    ax.set_xlim(centre[0] - half_range, centre[0] + half_range)
    ax.set_ylim(centre[1] - half_range, centre[1] + half_range)
    ax.set_zlim(centre[2] - half_range, centre[2] + half_range)

    trails = [ax.plot([], [], [], c=colours[i % len(colours)], linewidth=0.9)[0]
              for i in range(n_bodies)]
    markers = [ax.plot([], [], [], marker="o", ls="None", c=colours[i % len(colours)],
                       label=names[i])[0] for i in range(n_bodies)]
    fig.legend(loc="upper right", fontsize="small")

    def update(frame):
        for i in range(n_bodies):
            path = frames[:frame + 1, i]
            trails[i].set_data_3d(path[:, 0], path[:, 1], path[:, 2])
            markers[i].set_data_3d(path[-1:, 0], path[-1:, 1], path[-1:, 2])
        return trails + markers

    # cache_frame_data=False: frame indices are cheap to regenerate, no need to keep them
    anim = animation.FuncAnimation(fig, update, frames=n_frames, blit=False,
                                   repeat=False, cache_frame_data=False)

    start = time.time()
    last_reported = [-1]

    def progress(i, total):
        percent = 100 * (i + 1) // total
        if percent // 10 != last_reported[0]:
            last_reported[0] = percent // 10
            print(f"Rendering animation: {percent:3d}% ({i + 1}/{total} frames, "
                  f"{time.time() - start:.0f}s)", flush=True)

    try:
        anim.save(out_path, writer=writer, dpi=dpi, progress_callback=progress)
    finally:
        plt.close(fig)
    print(f"Animation saved to {out_path} in {time.time() - start:.1f}s")
    return out_path

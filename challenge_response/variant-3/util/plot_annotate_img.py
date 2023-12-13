
ax2 = fig.add_subplot(111,frame_on=False)
ax2.axis("off")
ax2.axis([0,1,0,1])
x, y = proj(points_x[172], points_y[172], points_z[172], ax, ax2)
image(ax2, drone_img_gray_file, [x, y])

def proj(x,y,z, ax1, ax2):
    """ From a 3D point in axes ax1,
        calculate position in 2D in ax2 """
    x2, y2, _ = proj3d.proj_transform(x,y,z, ax1.get_proj())
    return ax2.transData.inverted().transform(ax1.transData.transform((x2, y2)))

def image(ax,path,xy):
    """ Place an image (arr) as annotation at position xy """
    im = offsetbox.OffsetImage(plt.imread(path, format="png"), zoom=0.35)
    im.image.axes = ax
    ab = offsetbox.AnnotationBbox(im, xy,
                        xycoords='data', boxcoords="offset points",
                        pad=0.3, frameon=False)
    ax.add_artist(ab)

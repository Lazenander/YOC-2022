from pyecharts.charts import Map
from pyecharts import options as opts

def cnMap(filename, title, provincedata, nummin, nummax):
    Map(init_opts=opts.InitOpts(width = "1200px",
                                height = "800px")).add(
        label_opts = opts.LabelOpts(is_show=False),
        is_map_symbol_show=False,
        series_name = None,
        data_pair = provincedata,
        maptype = "china",
    ).set_global_opts(
        title_opts = opts.TitleOpts(title = title),
        visualmap_opts = opts.VisualMapOpts(
            min_ = nummin,
            max_ = nummax,
            is_piecewise = True
        ),
    ).render("./result/" + filename + ".html")
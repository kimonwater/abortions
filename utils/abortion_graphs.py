#### IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox # for emojis
import folium # for map
import squarify # for tree maps
import warnings # for suppressing

warnings.simplefilter("ignore") 


#### PRE-PROCESSING
# read csv
data_all = pd.read_csv("data/abortions_basetable_aggr_prev.csv", delimiter = ";")

# get 10y data
data = data_all[data_all["year"]>=2012]

# get cumsum
data["abortions_cumsum"] = data["abortions"].cumsum() 

# get abortions sum
data_cum = data.copy()
data_cum = data_cum.sum().to_frame().transpose()
del data_cum["year"]

#### STYLING
plt.rcParams["font.size"] = 6
plt.rcParams["font.family"] = "monospace"
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.titleweight"] = "semibold"


#### GET ABORTIONS BY YEAR AND CUMULATED
def years():
    x = data["year"]
    y_cum = data["abortions_cumsum"]
    y_abs = data["abortions"]

    fig, ax = plt.subplots()

    ax.plot(x, y_cum, color = "#E3DFFD", marker = "o", label = "abortions cumulated")
    plt.fill_between(x, y_cum, color = "#E3DFFD", alpha = .2)
    plt.bar(x, y_abs, color = "#ece3f0", label = "abortions by year")


    for a, b in zip(x, y_abs): 
        plt.text(a, b, str(b), size = 8, family = "monospace", horizontalalignment='center')
        
    image = plt.imread("babyemojidefault.png")
    image_box = OffsetImage(image, zoom=0.1)
    for x0, y0 in zip(x, y_cum): 
        ab = AnnotationBbox(image_box, (x0, y0), frameon=False)
        ax.add_artist(ab)
        plt.text(x0, y0, str(y0), size = 8, family = "monospace", verticalalignment = "bottom", horizontalalignment = "center")

    plt.title("Abortions in 10y")
    plt.legend()
    
    plt.yticks([])
    plt.xticks(x)

    for location in ["top", "right", "bottom", "left"]:
        ax.spines[location].set_color("lightgrey") 

    return plt.show()


#### GET ABORTIONS SIZED AS CITIES
def cities():

    # read csv and preprocess city, plz, population and lat-lon data
    population = pd.read_csv("data/cities_pop_preprocessed.csv", delimiter = ";")
    lonlat = pd.read_csv("data/cities_lonlat.csv", delimiter = ";")
    final = pd.merge(population, lonlat, left_on = "postal_code", right_on = "plz", how = "left")


    # create map 
    m = folium.Map(
        location=[51.2245166,10.3980907], # lat-lon of Muehlhausen, city kinda in the middle of Germany
        zoom_start=6, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ",
        min_zoom = 6,
        max_zoom = 8
        )

    # get and mark cities about 
    cities_about = final[final["category"] == "about"]

    for loc, p in zip(zip(cities_about["lat"], cities_about["lon"]), cities_about["city_name"]):
        folium.Marker(
            location=loc,
            icon=folium.DivIcon(html=f"""<div style="color:#000000;background:#efe7d3;width:60px;text-align:center;font-family: Courier New;">{p}</div>"""),
            # tooltip= "population: " + str(int(cities_about[cities_about["city_name"] == f"{p}"].population))
    ).add_to(m)
        
    # get and mark cities above with proportion
    df_proportion = final[final["population"] >= 1000000]

    df_proportion["proportion"] = round(100.0*(1004922/round(df_proportion["population"]))).astype(int)

    for loc, n, pr in zip(zip(df_proportion["lat"], df_proportion["lon"]), df_proportion["city_name"], df_proportion["proportion"]):
        folium.Marker(
            location=loc,
            icon=folium.DivIcon(html=f"""<div style="color:#000000;background:#E3DFFD;width:60px;text-align:center;font-family: Courier New;">{n} {pr}%</div>"""),
            # tooltip= "population: " + str(int(df_proportion[df_proportion["city_name"] == f"{n}"].population))
    ).add_to(m)
        
    return m

    
#### GET ABORTION DISTRIBUTIONS
def treemaps():
    ## CREATE FIG AND SUBPLOTS
    fig, ax = plt.subplots(5, 2, figsize = (8, 14))

    ## FIRST TREEMAP (ALL PREGNANCIES)
    # pre-set labels incl. proportions
    total = data_cum.loc[0]["live_births"] + data_cum.loc[0]["still_births"] + data_cum.loc[0]["abortions"]
    labels_size = []
    for column in ["live_births", "abortions", "still_births"]:
        value = data_cum.loc[0][column]
        labels_size.append(column + "\n" + str(round(value/1000000, 1)) + " mio" + " (" + str(round(value/total*100)) + "%)")

    # create treemap with squarify and style with pyplot
    squarify.plot(
        sizes = [data_cum["live_births"], data_cum["abortions"], data_cum["still_births"]], 
        label = labels_size, 
        color = ["#efe7d3", "#E3DFFD", "#E3DFFD"], 
        ax = ax[0][0])

    ax[0][0].axis("off")
    ax[0][0].set_title("Vs Newborns")

    ax[0][1].text(0, .5, "Under all newborns (live or still; not lost), every 8.5th is aborted. \nFor every 7.5 live births, there is 1 abortion.", horizontalalignment = "left")
    ax[0][1].axis("off")
        
    ## REMAINING 4 TREEMAPS (BY REASON, FAMILY STATUS, AGE GROUPS, PREVIOUS LIVE BIRTHS)
    # pre-set for iterating
    keywords = ["r", "f", "a", "p"]

    titleslist = ["By Reason", "By Family Status", "By Age Group", "By Previous Live Births"]

    descrlist = [
        "More than 96% of abortions are based on counseling. \nMedical & criminological indication are an edge case with 3.74 & 0.03%.",
        "57% of abortions are with single family status.",
        "Women from 18 to 30 make 50% of abortions. \nWomen from 18 to 35 total 73% of abortions. \nMinors make an edge case of 3% while 25% of abortions are 35yo+.",
        "40% of abortions are the woman's first child. \n24% are the 2nd child and 36% the 3rd plus."
    ]


    colors = ["#E3DFFD", "#efe7d3", "#e4e3e0", "#eaeff4"] # purple, beige, grey, blue 
    colors_age = ["#e4e3e0", "#eaeff4", "#E3DFFD", "#ece3f0", "#FAF6FF", "#efe7d3", "#F7F1E5", "#FFF9B6"] # lightpurple, lightpink, lightbeige, yellow
    colors_prev = ["#E3DFFD", "#eaeff4", "#e4e3e0", "#efe7d3", "#F7F1E5", "#FFF9B6"] 
    colorslist = [colors, colors, colors_age, colors_prev]

        
    # create treemaps by iterating 
    for keyword, i in zip(keywords, range(1,5)):
        labels = []
        sizes = []
        for column in data_cum.columns:
            if column.startswith(f"{keyword}_"):
                labels.append(f"{column[2:]} \n {round(data_cum.loc[0][column]/1000)}k ({str(round(data_cum.loc[0][column]/data_cum.loc[0][0]*100))}%)")
                sizes.append(data_cum[column])
        squarify.plot(sizes = sizes, label = labels, ax = ax[i][0], color = colorslist[i-1])
        ax[i][0].axis("off")
        ax[i][0].set_title(titleslist[i-1])
        ax[i][1].text(0, .5, descrlist[i-1], horizontalalignment = "left")
        ax[i][1].axis("off")

    return plt.show()
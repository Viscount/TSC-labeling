from app import app


@app.template_filter('playback_formation')
def playback_formation(playback_time):
    minutes = playback_time // 60
    seconds = playback_time - minutes * 60
    return '%02d:%05.2f' % (minutes, seconds)


@app.template_filter('label_formation')
def label_formation(label_int):
    if label_int == 10:
        label = 'Quality'
    elif label_int == 5:
        label = 'Normal'
    elif label_int == 1:
        label = 'Noise'
    else:
        label = 'None'
    return label

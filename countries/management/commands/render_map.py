from kartograph import Kartograph


def main():
    k = Kartograph()
    k.generate({
        'proj': {
            'id': 'ortho',
            'lon0': -97.7428,
            'lat0': 30.2669,
        },
        'layers': [{
            'special': 'sea',
            'styles': {
                'fill': 'D0DDF0',
            }
        }, {
            'id': 'countries',
            'src': 'countries/fixtures/countries/ne_10m_admin_0_sovereignty.shp',
            'styles': {
                'fill': 'EEE9E6',
            }
        }],
        'export': {
            'width': 300,
            'height': 300,
        }
    }, 'output.svg')


if __name__ == '__main__':
    main()

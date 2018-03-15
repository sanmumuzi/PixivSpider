import argparse


def process_args():
    parser = argparse.ArgumentParser(
        description='Download pictures for Pixiv Painter.'
    )
    parser.add_argument('-g', '--gui', action='store_true', help='Open the GUI.')
    parser.add_argument('-u', '--username', help='Your Pixiv_username.')
    parser.add_argument('-p', '--password', help='Your Pixiv_password.')
    # parser.add_argument('-pid', '--painter_id', help='Painter ID', required=True)
    parser.add_argument('-pid', '--painter_id', help='Painter ID')

    args = parser.parse_args()
    return dict(gui=args.gui, username=args.username, password=args.password, painter_id=args.painter_id)

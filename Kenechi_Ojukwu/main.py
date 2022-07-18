import os
import argparse
from detector.person import ExtractPerson
from seperator.seperate import PlayerSeparator



class Solution(object):

    def __init__(self, output_file=None, skip=False, skip_type="n_seconds"):
        self.output_file = output_file
        self.skip = skip
        self.skip_type = skip_type

    def remove_images_(self, diir):
        for image_path in os.listdir(diir):
            os.remove(image_path)


    def run(self):

        football_players = ExtractPerson(self.skip, self.skip_type)
        teams = PlayerSeparator(self.output_file)

        # extract the people in the video
        football_players.extract_person()

        # set directory variable
        diir = '/ps/challenge/players/'

        # seperate players into teams
        teams.seperate_players(diir)

        # clear players folder
        self.remove_images_(diir)


        print('Done!')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-op', '--output_path', action='store', type=str, required=False, help="Output Path")
    parser.add_argument('-s','--skip', action='store', type=str, required=False, help="skip frames")
    parser.add_argument('-st','--skip_type', action='store', type=str, required=False, help="what skipping algorithm type? n_frames or n_seconds")
    args = parser.parse_args()

    # url endpoint
    output_path = '/ps/challenge/result/'


    if args.output_path:
        result = Solution(output_file = args.output_path, skip=args.skip, skip_type=args.skip_type)
    else:
        result = Solution(output_file = output_path, skip=args.skip, skip_type=args.skip_type)

    result.run()




 
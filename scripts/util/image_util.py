import imageio
import os

class ImageUtil:
    
    @staticmethod
    def convert_images_to_gif(path, duration):
        """
        Constructs an animated gif from the list of static images.

        :parameters:
            path (string): path to the file
            duration (int): the duration between frame in milliseconds
        """
        image_folder = os.fsencode(path)
        filenames = []
        for filename in os.listdir(image_folder):
            filename = os.fsdecode(filename)
            if filename.endswith( ('.jpeg', '.png', '.gif') ):
                filename = os.path.join(path, filename)
                filenames.append(filename)
        
        # TODO use PIL to add transparency
        images = list(map(lambda image: imageio.imread(image), filenames))

        outputfile = 'heatmaps_over.gif'
        imageio.mimsave(outputfile, images, duration=duration/1000)
        return outputfile
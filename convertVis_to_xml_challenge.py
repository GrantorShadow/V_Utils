# convert Visdrone to PASCAL-VOC
import os
from tqdm import tqdm
from PIL import Image
import argparse


def convert(args):

	os.makedirs(args.output_img_folder, exist_ok=True)
	os.makedirs(args.output_ann_folder, exist_ok=True)

	for im in tqdm(os.listdir(args.input_img_folder)):
		xml_annotation = im.split('.jpg')[0] + '.xml'
		xml_path = os.path.join(os.getcwd(), args.output_ann_folder, xml_annotation)

		img_file = im.split('.jpg')[0] + '.jpg'
		img_path = os.path.join(os.getcwd(), args.input_img_folder, img_file)
		output_img_path = os.path.join(os.getcwd(), args.output_img_folder, img_file)

		img = Image.open(img_path)
		annotation_string_init = '''
	<annotation>
		<folder>annotations</folder>
		<filename>{}</filename>
		<path>{}</path>
		<source>
			<database>Unknown</database>
		</source>
		<size>
			<width>{}</width>
			<height>{}</height>
			<depth>{}</depth>
		</size>
		<segmented>0</segmented>'''.format(img_file, img_path, img.size[0], img.size[1], len(img.mode))

		annotation_string_init = annotation_string_init
		img.save(output_img_path)
		annotation_string_final = annotation_string_init + '</annotation>'
		f = open(xml_path, 'w')
		f.write(annotation_string_final)
		f.close()


def main():
	parser = argparse.ArgumentParser(
		description='This script support converting voc format xmls to coco format json')
	parser.add_argument(
		'--input_img_folder', type=str, default=None, help='path to img files directory')
	parser.add_argument(
		'--output_img_folder', type=str, default=None, help='path of output img')
	parser.add_argument(
		'--output_ann_folder', type=str, default=None, help='path to output xml ann.')

	args = parser.parse_args()

	convert(args)


if __name__ == '__main__':
	main()

# convert Visdrone to PASCAL-VOC
import os
from tqdm import tqdm
from PIL import Image, ImageDraw
import argparse


# removed the 0,11 keys, since they are useless
label_dict = {
	"1": "Pedestrian",
	"2": "People",
	"3": "Bicycle",
	"4": "Car",
	"5": "Van",
	"6": "Truck",
	"7": "Tricycle",
	"8": "Awning-tricycle",
	"9": "Bus",
	"10": "Motor"
}


def upscale_img(sizing, img):
	if sizing != None:
		sizing = int(sizing)
		w, h = img.size
		x_scale, y_scale = sizing / w, sizing / h
		up_scaled_img = img.resize((sizing, sizing))
		return up_scaled_img, x_scale, y_scale
	return img, 1, 1

def object_string(label, bbox):
	req_str = '''
	<object>
		<name>{}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{}</xmin>
			<ymin>{}</ymin>
			<xmax>{}</xmax>
			<ymax>{}</ymax>
		</bndbox>
	</object>
	'''.format(label, bbox[0], bbox[1], bbox[2], bbox[3])
	return req_str


def convert(args):
	count = 0

	# try 1024, 1080, 1920, 2048

	os.makedirs(args.output_img_folder, exist_ok=True)
	os.makedirs(args.output_ann_folder, exist_ok=True)

	annotation_list = os.listdir(args.input_ann_folder)

	for annotation in tqdm(annotation_list):
		annotation_path = os.path.join(os.getcwd(), args.input_ann_folder, annotation)
		xml_annotation = annotation.split('.txt')[0] + '.xml'
		xml_path = os.path.join(os.getcwd(), args.output_ann_folder, xml_annotation)
		img_file = annotation.split('.txt')[0] + '.jpg'
		img_path = os.path.join(os.getcwd(), args.input_img_folder, img_file)
		output_img_path = os.path.join(os.getcwd(), args.output_img_folder, img_file)
		img = Image.open(img_path)
		# scaling the image by the sizing value
		img, x_scale, y_scale = upscale_img(args.sizing, img)
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

		file = open(annotation_path, 'r')
		lines = file.readlines()
		for line in lines:
			new_line = line.strip('\n').split(',')
			new_coords_min = (
				int(int(new_line[0]) * x_scale), int(int(new_line[1]) * y_scale)
			)
			new_coords_max = (
				int(int(new_line[0]) * x_scale) + int((int(new_line[2]) * x_scale)),
				int((int(new_line[1]) * y_scale)) + int(int(new_line[3]) * y_scale)
			)
			bbox = (
				int(int(new_line[0]) * x_scale), int(int(new_line[1]) * y_scale),
				int(int(new_line[0]) * x_scale) + int(int(new_line[2]) * x_scale),
				int(int(new_line[1]) * y_scale) + int(int(new_line[3]) * y_scale)
			)
			label = label_dict.get(new_line[5])
			req_str = object_string(label, bbox)
			annotation_string_init = annotation_string_init + req_str

			if args.show_annotations:
				img1 = ImageDraw.Draw(img)
				img1.rectangle([new_coords_max, new_coords_min], outline="blue")

		img.save(output_img_path)
		annotation_string_final = annotation_string_init + '</annotation>'
		f = open(xml_path, 'w')
		f.write(annotation_string_final)
		f.close()
		count += 1

	print('[INFO] Completed {} image(s) and annotation(s) pair & Upscaled to : {} x {}'.format(
		count, args.sizing, args.sizing)
	)


def main():
	parser = argparse.ArgumentParser(
		description='This script support converting voc format xmls to coco format json')
	parser.add_argument(
		'--input_img_folder', type=str, default=None, help='path to img files directory')
	parser.add_argument(
		'--input_ann_folder', type=str, default=None, help='path to annotation files ')
	parser.add_argument(
		'--output_img_folder', type=str, default=None, help='path of output img')
	parser.add_argument(
		'--output_ann_folder', type=str, default=None, help='path to output xml ann.')
	parser.add_argument(
		'--sizing', type=str, default=None, help='upscale the image to ; None means no upscaling')
	parser.add_argument(
		'--show_annotations', type=str, default=False, help='shows markings')

	args = parser.parse_args()

	convert(args)


if __name__ == '__main__':
	main()

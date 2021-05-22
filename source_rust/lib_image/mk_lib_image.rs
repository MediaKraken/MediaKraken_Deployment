// image 0.23.14
use image::GenericImageView;

pub fn mk_image_file_resize(base_image_path: &str,
                            image_save_path: &str,
                            width: u32, height: u32) {
    let tiny = image::open(base_image_path).unwrap();
    let scaled = tiny.resize(width, height, FilterType::Nearest);
    let mut output = File::create(image_save_path).unwrap();
    scaled.write_to(&mut output, ImageFormat::Png).unwrap();
}
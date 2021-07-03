
pub fn mk_image_file_resize(base_image_path: &str,
                            image_save_path: &str,
                            width: u32, height: u32) {
    let tiny = image::open(base_image_path).unwrap();
    let scaled = tiny.resize(width, height, image::imageops::FilterType::Nearest);
    let mut output = std::fs::File::create(image_save_path).unwrap();
    scaled.write_to(&mut output, image::ImageFormat::Png).unwrap();
}

// cargo test -- --show-output
#[cfg(test)]
mod test_mk_lib_common {
    use super::*;

    macro_rules! aw {
    ($e:expr) => {
        tokio_test::block_on($e)
    };
  }
}
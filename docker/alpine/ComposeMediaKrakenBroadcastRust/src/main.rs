use bollard::Docker;
use bollard::image::ListImagesOptions;

use futures_util::future::FutureExt;

use std::default::Default;

async fn main() {
    let images = &docker.list_images(Some(ListImagesOptions::<String> {
        all: true,
        ..Default::default()
    })).await.unwrap();

    for image in images {
        println!("-> {:?}", image);
    }
};

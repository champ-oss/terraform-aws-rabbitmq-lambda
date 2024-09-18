data "aws_region" "this" {}

resource "random_id" "this" {
  byte_length = 3
}

data "archive_file" "this" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir      = "${path.module}/src"
  output_path      = "${path.module}/package.zip"
}

# img_crop_from_PDF
PDF파일에서 이미지만 추출합니다.
벡터 그래픽이나 메모, 하이라이트는 추출되지 않습니다.


## Dependnecy
Pillow와 PymuPDF 라이브러리가 필요합니다.

> pip install pillow pymupdf


## ussage
> python main.py \<pdf file to extract> \<output directory>

## sample
> python main.py sample.pdf result

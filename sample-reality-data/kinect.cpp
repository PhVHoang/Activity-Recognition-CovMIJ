#include<bits/stdc++.h>
#include <opencv2/opencv.hpp>
using namespace std;
using namespace cv;

static Mat create_depth_vis(Mat depth){
		Mat gray(depth.size(), CV_8UC1);
		gray.setTo(0);
		Mat vis(depth.size(), CV_8UC3);
		vis.setTo(0);
		for (int i = 0; i < depth.rows;i++)
		for (int j = 0; j < depth.cols; j++)
		{
			uint16_t val = depth.at<uint16_t>(i,j);
			char gray_val = 255-val >> 8;
			gray.at<char>(i, j) = gray_val;
		}

		applyColorMap(gray, vis, COLORMAP_JET);
		imshow("vis_depth", vis);
		waitKey(1);
		return vis;
	}


Mat get_depth(ifstream &depth_reader){
	Mat depth;
	if (!depth_reader.eof())
	{
		int size;
		depth_reader.read(reinterpret_cast<char *>(&size), 4);
		vector<uchar> fileData(size);
		depth_reader.read((char*)&fileData[0], size);



		depth = imdecode(Mat(fileData), IMREAD_ANYDEPTH);

		if (depth.data != NULL){
			depth = create_depth_vis(depth);
		}
	}
	return depth;
}


int main(int argc, const char* argv[]) {
	ifstream reader("depth.bin", ios::in | ios::binary);
	while (true){
		Mat depth=get_depth(reader);
		if(depth.data==NULL) break;
	}
	return 0;
}

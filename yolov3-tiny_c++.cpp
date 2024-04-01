#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <vector>

int main() {
    // Load YOLO model and COCO class names
    cv::dnn::Net net = cv::dnn::readNet("yolov3-tiny.weights", "yolov3-tiny.cfg");
    std::ifstream classFile("coco.names");
    std::vector<std::string> classes;
    std::string className;
    while (std::getline(classFile, className)) {
        classes.push_back(className);
    }

    // Initialize the webcam capture (you can use 0 for the default camera)
    cv::VideoCapture cap(0);

    // Initialize variables for FPS calculation
    int frame_count = 0;
    double start_time = cv::getTickCount() / cv::getTickFrequency();

    while (true) {
        cv::Mat frame;
        cap.read(frame);
        
        if (frame.empty()) {
            break;
        }

        int Width = frame.cols;
        int Height = frame.rows;

        // Create input blob
        cv::Mat blob = cv::dnn::blobFromImage(frame, 0.00392, cv::Size(320, 320), cv::Scalar(0, 0, 0), true, false);

        // Set input blob for the network
        net.setInput(blob);

        // Run inference through the network and gather predictions from output layers
        std::vector<cv::Mat> outs;
        net.forward(outs, net.getUnconnectedOutLayersNames());

        std::vector<int> class_ids;
        std::vector<float> confidences;
        std::vector<cv::Rect> boxes;

        // Create bounding boxes
        for (const auto& out : outs) {
            for (int i = 0; i < out.rows; i++) {
                cv::Mat detection = out.row(i);

                float* scores = (float*)detection.data + 5;
                int class_id = std::max_element(scores, scores + 80) - scores;
                float confidence = scores[class_id];

                if (confidence > 0.1) {
                    float center_x = detection.at<float>(0) * Width;
                    float center_y = detection.at<float>(1) * Height;
                    float w = detection.at<float>(2) * Width;
                    float h = detection.at<float>(3) * Height;
                    float x = center_x - w / 2;
                    float y = center_y - h / 2;
                    class_ids.push_back(class_id);
                    confidences.push_back(confidence);
                    boxes.push_back(cv::Rect(x, y, w, h));
                }
            }
        }

        std::vector<int> indices;
        cv::dnn::NMSBoxes(boxes, confidences, 0.1, 0.1, indices);

        for (size_t i = 0; i < indices.size(); i++) {
            int item = indices[i];
            cv::Rect box = boxes[item];
            if (class_ids[item] == 0) {  // Person class
                std::string label = classes[class_ids[item]];
                cv::rectangle(frame, box, cv::Scalar(0, 0, 0), 2);
                cv::putText(frame, label, cv::Point(box.x - 10, box.y - 10), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0), 2);
            }
        }

        // Calculate FPS
        frame_count++;
        double end_time = cv::getTickCount() / cv::getTickFrequency();
        double elapsed_time = end_time - start_time;
        double fps = frame_count / elapsed_time;

        // Display FPS on the frame
        cv::putText(frame, "FPS: " + std::to_string(fps), cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 0, 0), 2);

        // Display the processed frame
        cv::imshow("Webcam", frame);

        // Press 'q' to exit the loop
        if (cv::waitKey(1) == 'q') {
            break;
        }
    }

    // Release the webcam and close all OpenCV windows
    cap.release();
    cv::destroyAllWindows();

    return 0;
}

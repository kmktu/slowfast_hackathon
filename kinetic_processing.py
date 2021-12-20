import os
import subprocess
import json
import csv
import math
import shutil

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' +  directory)

def load_json_event(json_path):
    events = []
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf8') as json_f:
            json_data = json.load(json_f)

            events = json_data["events"]
    else:
        with open("./error.txt", 'w', encoding='utf8') as error_f:
            error_f.write(json_path + "\n")
        print("Error : not matched " + json_path)

    return events

def write_csv(output_dir, class_no, output_mp4):
    global split_dict

    output_mp4 = r"/mnt/learning_mount/slowfast_train/preprocessing_kinetic/data/kinetic_fmt2/" + output_mp4

    if int(class_no) >= 30:
        class_no = str(int(class_no) - 22)
    else:
        class_no = str(int(class_no) - 1)

    if split_dict[class_no] % 10 == 0:
        with open(output_dir + "test.csv", "a", encoding='utf8') as test_f:
            test_f.write(output_mp4 + " " + class_no + "\n")
        split_dict[class_no] = 1
    elif split_dict[class_no] % 9 == 0:
        with open(output_dir + "val.csv", "a", encoding='utf8') as val_f:
            val_f.write(output_mp4 + " " + class_no + "\n")
        split_dict[class_no] += 1
    else:
        with open(output_dir + "train.csv", "a", encoding='utf8') as train_f:
            train_f.write(output_mp4 + " " + class_no + "\n")
        split_dict[class_no] += 1

def run_ffmpeg(events, json_path, file_name):
    if len(events) != 0:
        global output_dir
        count = 1
        class_no = file_name.split("_")[1]
        if class_no in class_dict.keys():
            createFolder(output_dir + class_dict[class_no])

        for event in events:
            # input_mp4 = json_path.replace("json_action","mp4")
            input_mp4 = json_path + "\\" + file_name + ".mp4"
            output_mp4 = class_dict[class_no] + "/" + file_name + "_%03d.mp4"% (count)
            count += 1
            cmd = 'ffmpeg -n -i ' + input_mp4 + ' -an -compression_algo raw -r 3 -filter_complex select=between(n\\,' \
                  + str(event["ev_start_frame"]) + '\\,' + str(event["ev_end_frame"]) + '\\),setpts=PTS-STARTPTS ' + output_dir + output_mp4
            print(cmd)
            subprocess.run(cmd)
            write_csv(output_dir, class_no, output_mp4)

def processing(label_folder):
    for root, dirs, files in os.walk(label_folder):
        for file in files:
            file_name, extension = os.path.splitext(file)
            if extension.lower() == ".json":
                print("processing: ", file)
                json_path = root
                events = load_json_event(root + "/" + file)

                run_ffmpeg(events, json_path, file_name)


def read_mp4_to_csv(output_dir):
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            file_name, ext = os.path.splitext(file)
            if ext == ".mp4":
                print(file_name)
                if file_name.split("_")[1] == "1":
                    count_dict["0"] += 1
                elif file_name.split("_")[1] == "2":
                    count_dict["1"] += 1
                elif file_name.split("_")[1] == "3":
                    count_dict["2"] += 1
                elif file_name.split("_")[1] == "4":
                    count_dict["3"] += 1
                elif file_name.split("_")[1] == "5":
                    count_dict["4"] += 1
                elif file_name.split("_")[1] == "6":
                    count_dict["5"] += 1
                elif file_name.split("_")[1] == "7":
                    count_dict["6"] += 1
                elif file_name.split("_")[1] == "8":
                    count_dict["7"] += 1
                elif file_name.split("_")[1] == "30":
                    count_dict["8"] += 1
                elif file_name.split("_")[1] == "31":
                    count_dict["9"] += 1
                elif file_name.split("_")[1] == "32":
                    count_dict["10"] += 1
                elif file_name.split("_")[1] == "33":
                    count_dict["11"] += 1

    write_format = "/mnt/learning_mount/slowfast_train/preprocessing_kinetic/data/kinetic_fmt2"
    smoking_count = 0
    fishing_count = 0
    trash_dump_count = 0
    wall_over_count = 0
    damage_to_facilities_count = 0
    banner_action_count = 0
    fliers_action_count = 0
    tent_setup_count = 0
    sit_down_bench_count = 0
    sit_down_floor_count = 0
    moving_count = 0
    stand_count = 0
    train_csv = open(output_dir + "/train.csv", 'w', newline='')
    train_wr = csv.writer(train_csv)
    val_csv = open(output_dir + "/val.csv", 'w', newline='')
    val_wr = csv.writer(val_csv)
    test_csv = open(output_dir + "/test.csv", 'w', newline='')
    test_wr = csv.writer(test_csv)

    for root, dirs, files in os.walk(output_dir):
        for file in files:
            file_name, ext = os.path.splitext(file)
            if ext == ".mp4":
                if file_name.split("_")[1] == "1":
                    smoking_count += 1
                    dict_str = "0"
                    write_csv_count(smoking_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "2":
                    fishing_count += 1
                    dict_str = "1"
                    write_csv_count(fishing_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "3":
                    trash_dump_count += 1
                    dict_str = "2"
                    write_csv_count(trash_dump_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "4":
                    wall_over_count += 1
                    dict_str = "3"
                    write_csv_count(wall_over_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "5":
                    damage_to_facilities_count += 1
                    dict_str = "4"
                    write_csv_count(damage_to_facilities_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "6":
                    banner_action_count += 1
                    dict_str = "5"
                    write_csv_count(banner_action_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "7":
                    fliers_action_count += 1
                    dict_str = "6"
                    write_csv_count(fliers_action_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "8":
                    tent_setup_count += 1
                    dict_str = "7"
                    write_csv_count(tent_setup_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "30":
                    sit_down_bench_count += 1
                    dict_str = "8"
                    write_csv_count(sit_down_bench_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "31":
                    sit_down_floor_count += 1
                    dict_str = "9"
                    write_csv_count(sit_down_floor_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "32":
                    moving_count += 1
                    dict_str = "10"
                    write_csv_count(moving_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)
                elif file_name.split("_")[1] == "33":
                    stand_count += 1
                    dict_str = "11"
                    write_csv_count(stand_count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str)


def write_csv_count(count, file_name, train_wr, val_wr, test_wr, write_format, root, dict_str):

    if count <= math.ceil(count_dict[dict_str] * 0.8):
        train_wr.writerow([write_format + "/" + root.split("/")[-1] + "/" + file_name + ".mp4" + " " + dict_str])
    elif count > math.ceil(count_dict[dict_str] * 0.8):
        if count <= math.ceil(count_dict[dict_str] * 0.8 + count_dict[dict_str] * 0.1):
            val_wr.writerow([write_format + "/" + root.split("/")[-1] + "/" + file_name + ".mp4" + " " + dict_str])
        elif count > math.ceil(count_dict[dict_str] * 0.8 + count_dict[dict_str] * 0.1):
            test_wr.writerow([write_format + "/" + root.split("/")[-1] + "/" + file_name + ".mp4" + " " + dict_str])


def copy_mp4_to_json_folder():
    json_path = r"Z:/slowfast_train/completed_json3/json_mp4"
    mp4_path = "Z:/1.Data"
    mp4_filtering_folder = ["2.불법객체", "3.정상객체", "객체_정제완료_미사용클립(2개이상등)",
                            "객체_정제완료_삭제클립", "영상_기존촬영_잔여분클립(손가락)", "해커톤대회 이미지 제출(13,000장)",
                            "객체_2개이상_업로드완료"]
    json_list = []
    for root, dirs, files in os.walk(json_path):
        for file in files:
            file_name, ext = os.path.splitext(file)
            if ext == ".json":
                print("json_list_up : ", file)
                json_list.append(file_name)
    i = 0
    for root, dirs, files in os.walk(mp4_path):
        dirs[:] = [dir for dir in dirs if dir.lower() not in mp4_filtering_folder]
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == ".mp4":
                if filename in json_list:
                    if not os.path.exists(json_path + "/" + file):
                        print("copy mp4 : ", file + " --------------- ", i, "/", len(json_list))
                        shutil.copy(root + "/" + file, json_path)
                    i+=1

if __name__ == "__main__":
    class_dict = {"1": "smoking", "2": "fishing", "3": "trash_dump", "4": "wall_over", "5": "damage_to_facilities", "6": "banner_action",
                  "7": "fliers_action", "8": "tent_setup", "30": "sit_down_bench", "31": "sit_down_floor", "32": "moving", "33": "stand"}
    split_dict = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1,"5": 1,
                  "6": 1, "7": 1, "8": 1, "9": 1,"10": 1, "11": 1}

    count_dict = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0,"5": 0,
                  "6": 0, "7": 0, "8": 0, "9": 0,"10": 0, "11": 0}

    # copy_mp4_to_json_folder()

    output_dir = r"Z:/slowfast_train/preprocessing_kinetic/data/kinetic_fmt2/"
    label_folder = r"Z:/slowfast_train/completed_json3/json_mp4"
    # createFolder(output_dir)
    #
    # processing(label_folder)
    #
    read_mp4_to_csv(output_dir)


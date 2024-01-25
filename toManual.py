import os


def read_and_convert_txt(directory, page_size=9):
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    files_processed = 0
    file_counter = 0

    # Get all the text files in the directory
    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    total_files = len(text_files)

    # Calculate the number of output files needed
    number_of_output_files = total_files // page_size + (1 if total_files % page_size else 0)

    for output_file_number in range(1, number_of_output_files + 1):
        # Construct the output file name with padded numbers
        start_index = (output_file_number - 1) * page_size + 1
        end_index = min(output_file_number * page_size, total_files)
        output_file_name = f'output_guide_{str(start_index).zfill(3)}-{str(end_index).zfill(3)}.txt'

        with open(output_file_name, 'w', encoding='utf-8') as txt_file:
            # Write a subset of files to each output file
            for file in text_files[file_counter:file_counter + page_size]:
                file_path = os.path.join(directory, file)

                with open(file_path, 'r', encoding='utf-8') as content_file:
                    txt_file.write(f"[h2] {file} [/h2]\n[code]\n")
                    txt_file.write(content_file.read())
                    txt_file.write("[/code]\n\n")

                files_processed += 1
                if files_processed >= total_files:
                    break

            file_counter += page_size


# Run the function for directory
read_and_convert_txt('txt/Lv3')
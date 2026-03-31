import os

TARGET_EXTENSIONS = (
    ".doc",
    ".docx",
    ".pdf",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".jpg",
    ".png",
    ".txt",
    ".lab",
)

USER_HOME = os.environ.get("USERPROFILE")
TARGET_FOLDERS = [
    os.path.join(
        USER_HOME, r"Documents\MacEwan University Classes\CMPT 380\Final_Project_Code"
    ),
    # os.path.join(USER_HOME, "Downloads"),
    # os.path.join(USER_HOME, "Pictures"),
    # os.path.join(USER_HOME, "Videos"),
]


def scan_files():
    found_files = []
    print(USER_HOME)

    for folder in TARGET_FOLDERS:
        if not os.path.exists(folder):
            continue

        for root, dir, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(TARGET_EXTENSIONS):

                    file_name = file
                    file_path = os.path.join(root, file)

                    found_files.append({"name": file_name, "path": file_path})

    return found_files

import streamlit as st
import json
from typing import List, Dict

# Paths to JSON files
JSON_FILE_PATH = "testcases.json"
LABELS_FILE_PATH = "labels.json"
TOKENS_FILE_PATH = "tokens.json"

def load_json(file_path: str) -> List[Dict]:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_json(data: List[Dict], file_path: str):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Load existing test cases, labels, and tokens
test_cases = load_json(JSON_FILE_PATH)
labels = load_json(LABELS_FILE_PATH)
tokens = load_json(TOKENS_FILE_PATH)

if not labels:
    labels = ["Algebra", "Calculus", "Geometry", "Statistics", "Other"]

# Authentication
st.title("Sign In")
token = st.text_input("Enter your token", type="password")
if st.button("Sign In"):
    if token in tokens:
        st.success("Sign in successful!")
        st.session_state["authenticated"] = True
    else:
        st.error("Invalid token. Please try again.")

if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.title("Test Case Submission")

    st.write("A text box where problems can be pasted and edited")
    problem = st.text_area("Problem", "")

    st.write("A text box where expected output is entered")
    expected_output = st.text_area("Expected Output", "")

    st.write("A check list where you can specify what kind of question it is")
    label = st.selectbox("Label", labels)

    if st.button("Submit"):
        new_test_case = {
            "problem": problem,
            "expected_output": expected_output,
            "mathgpt_output": "",
            "image_file_path": "",
            "label": label
        }
        test_cases.append(new_test_case)
        save_json(test_cases, JSON_FILE_PATH)
        st.success("Test case submitted successfully!")

    # Functionality to add a new label
    st.write("## Manage Labels")
    new_label = st.text_input("Add a new label")
    if st.button("Add Label"):
        if new_label and new_label not in labels:
            labels.append(new_label)
            save_json(labels, LABELS_FILE_PATH)
            st.success(f"Label '{new_label}' added successfully!")
        elif new_label in labels:
            st.warning(f"Label '{new_label}' already exists.")
        else:
            st.warning("Label cannot be empty.")

    # Functionality to remove an existing label
    label_to_remove = st.selectbox("Remove a label", labels)
    if st.button("Remove Label"):
        if label_to_remove in labels:
            labels.remove(label_to_remove)
            save_json(labels, LABELS_FILE_PATH)
            st.success(f"Label '{label_to_remove}' removed successfully!")

    # Display existing test cases (optional)
    st.write("## Existing Test Cases")
    st.write(test_cases)
# date_utils.py 
# Description: A Streamlit authentication demonstration application
# Copyright 2024 Michael Konrad 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Date: 2024-07-02

from datetime import datetime

def convert_date(date=datetime.now(), format='%m/%d/%Y'):
    """
    Converts a datetime object to a string in the provided format.

    Args:
        date (datetime): the datetime object to be converted
        format (string): the format to be produced

    Returns:
        string: the formatted date
    """
    return date.strftime(format)


def convert_epoch(time_stamp, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strftime(datetime.fromtimestamp(time_stamp), format)
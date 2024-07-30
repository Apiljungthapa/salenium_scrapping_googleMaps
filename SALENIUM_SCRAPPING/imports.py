# Common imports used across different modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import re
from urllib.parse import urlparse
from time import sleep
import time

# Imports for the GUI application
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor
import threading
import keyboard
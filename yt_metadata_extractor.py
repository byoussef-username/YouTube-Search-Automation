import threading
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ping3 import ping
import csv

import time


def sw(p):
    time.sleep(p)


class YTVIDSEARCH:
    def __init__(self, video_name, video_numeration=None):
        self.video_name = video_name
        self.video_numeration = video_numeration
        self.driver = uc.Chrome(version_main=147)
        self.stop_ping = False

    def monitor_ping(self):
        self.stop_ping = False
        lowest_latency = None
        avg_latency = 0
        highest_latency = None
        time_ping = 0
        while not self.stop_ping:

            sw(0.5)
            result = ping("youtube.com")
            time_ping += 1
            avg_latency += result
            if lowest_latency is None or result < lowest_latency:
                lowest_latency = result
            if highest_latency is None or result > highest_latency:
                highest_latency = result
            if result is False:
                print("Ping: Request timed out : No response from the server")
            elif result * 1000 > 300:
                print(
                    f"Ping: {result * 1000}ms : High latency detected, may affect scraping")
        else:
            print("Ping monitoring stopped.")
            print(f"Lowest Latency: {lowest_latency * 1000:.2f} ms")
            print(f"Average Latency: {(avg_latency/time_ping) * 1000:.2f} ms")
            print(f"Highest Latency: {highest_latency * 1000:.2f} ms")

    def main(self):
        t = threading.Thread(target=self.monitor_ping)
        try:

            t.start()

            wait = WebDriverWait(self.driver, 10)
            self.driver.get("https://youtube.com")
            search_bar = wait.until(
                EC.element_to_be_clickable((By.NAME, "search_query")))
            search_bar.send_keys(self.video_name)
            search_bar.send_keys(Keys.ENTER)
            sw(3)
            videos = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a#video-title")))
            channels = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ytd-channel-name#channel-name a")))
            video_views_and_update_times = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.inline-metadata-item.style-scope.ytd-video-meta-block")))

            print(f"video length: {len(videos)}")
            print(f"channel length: {len(channels)}")
            biggest = max(len(videos), len(channels))
            print(f"biggest category: {biggest}")
            minimum = min(len(videos), len(channels), len(
                video_views_and_update_times)//2)
            print(f"video total : {minimum}")
            videos_csv = []
            for i in range(minimum):
                videos_csv.append([videos[i].get_attribute("title"), videos[i].get_attribute("href"), channels[i].get_attribute("textContent"), channels[i].get_attribute(
                    "href"), video_views_and_update_times[i*2].get_attribute('textContent'), video_views_and_update_times[i*2+1].get_attribute('textContent')])
                print("-"*50)
                print(f"video number : {i+1}")
                print(f"title :{videos[i].get_attribute('title')}")
                print(f"vd link :{videos[i].get_attribute('href')}")
                print(f"channel :{channels[i].get_attribute('textContent')}")
                print(f"channel link:{channels[i].get_attribute('href')}")
                print(
                    f"views: {video_views_and_update_times[i*2].get_attribute('textContent')}")
                print(
                    f"update time: {video_views_and_update_times[i*2+1].get_attribute('textContent')}")
                print("-"*50)

            # CSV write moved outside the loop — no longer re-writing the file on every iteration
            with open('youtube_results.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Video Link", "Channel", "Channel Link",
                                 "Views", "Uploaded Time"])
                writer.writerows(videos_csv)

            print("File saved!")
        except Exception as e:
            if t.is_alive():
                print("alive Stopping ping thread due to an error.")
            else:
                print("dead Ping thread already stopped.")
            self.stop_ping = True
            print(f"Error starting the driver: {e}")

        finally:
            self.stop_ping = True
            t.join()


video1 = YTVIDSEARCH("python programming")
video1.main()
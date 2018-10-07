# -*- coding: utf-8 -*-
from selenium import webdriver
import  time ,re,sys ,winsound,os
from selenium.webdriver.common.alert import Alert



def get_stroke():
	chrome_options = webdriver.ChromeOptions()
	prefs = {
		'profile.default_content_setting_values': {
			'images': 2,  # 不加载图片
			'javascript': 2,  # 不加载JS
		}
	}

	chrome_options.add_experimental_option("prefs", prefs)
	chrome_options.add_argument('--ignore-certificate-errors')
	#chrome_options.add_argument('headless')

	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.implicitly_wait(30)
	tgts=[]
	try:
		fo = open("tgts.txt", "r+")
		while 1:
			line=fo.readline()
			tgts.append(line)
			if not line:
				break
	except:
		driver.get("https://zidian.51240.com/pinyinl/")
		message = driver.find_elements_by_class_name("list_zidian")
		urls=[]
		for i in message:
			for j in i.text.split():
				if j[0] =="e":
					urls.append("https://zidian.51240.com/"+j+"__pinyinl/")
		print(urls)
		for url in urls:
			driver.get(url)
			title = driver.find_element_by_class_name("h2dabiaoti").text
			print(title)
			continue_link = driver.find_elements_by_link_text('笔画')
			for n in continue_link:
				tgts.append(n.get_attribute("href"))
		fo = open("tgts.txt", "w")
		for tgt in tgts:
			fo.write(tgt+'\n')
		fo.close()

	strokes=[]
	flags=1

	try:
		f_stroke = open("strokes.txt", "r+")
		while 1:
			line=f_stroke.readline()
			strokes.append(line)
			if not line:
				break
		if abs(len(strokes)-len(tgts))<1000:
			flags=0
		f_stroke.close()
	except:
		pass
	if flags==1:
		try:
			os.remove("strokes.txt")
		except:
			pass
		f_stroke = open("strokes.txt", "w")
		counter=1
		for tgt in tgts:
			if counter <0:
				counter += 1
				print(tgt)
				continue
			driver.get(tgt)
			try:
				Alert(driver).accept()
			except:
				pass
			zifu=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td[2]').text[:1].replace("\n","")
			bihua=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[6]/td[2]').text.replace("更多：","").replace("\n","")
			strokes.append(zifu+":"+bihua)
			print(str(counter)+":  "+zifu+":"+bihua)
			counter += 1
			if counter % 100 == 0 :
				for stroke in strokes:
					try:
						f_stroke.write(stroke.replace("\n","")+'\n')
					except:
						pass
				strokes=[]
				f_stroke.close()
				f_stroke = open("strokes.txt", "a")



def main():
	get_stroke()

if __name__ == "__main__":
	main()
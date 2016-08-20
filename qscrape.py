#checks for stats in a quora profile
import numpy as np
import requests,sys,time,webbrowser,bs4,re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
# convert numbers like 2.1k in 2100
def format_num(num):
	rexp = re.compile('^.*k$')
	p = rexp.match(num)   #if the number is of the form x.yk
	if p:
		mynum = []   # store in a list
		numstr = ""  # convert to string
		numval = 0   #finally parse as number
		point_found = False
		for chr in num:
			if chr=='.':
				point_found = True
				mynum.append('000')
				numstr = ''.join(mynum)
				numval = int(numstr)
			if not point_found:
				mynum.append(chr)
			elif chr!='.' and chr!='k':
				numval = numval + (int(chr)*100)
		return numval
	else:
		return int(num)



#start
browser = webdriver.Chrome()
#login into google before opening quora
browser.get('https://www.gmail.com')


emailElem = browser.find_element_by_id('Email')
emailElem.send_keys('myusername') #the username
nextButton = browser.find_element_by_id('next')
nextButton.click()
time.sleep(2)
passwordElem = browser.find_element_by_id('Passwd')
passwordElem.send_keys('mypassWoRd')   #the password
signinButton = browser.find_element_by_id('signIn')
signinButton.click()
time.sleep(20)







myurl = 'https://www.quora.com/profile/'+' '.join(sys.argv[1:])
browser.get(myurl)
time.sleep(4)
browser.get(myurl)
time.sleep(6)

elem = browser.find_element_by_tag_name("body")
no_of_pagedowns = 20  #can be increased further

while no_of_pagedowns:
	elem.send_keys(Keys.PAGE_DOWN)
	time.sleep(0.8)
	no_of_pagedowns-=1

rawSource = browser.page_source


#get the soup
soup = bs4.BeautifulSoup(rawSource)

views = soup.select('.meta_num')
upvotes = soup.select('.count')

answersdiv = soup.body.find('div',attrs={'class':'layout_3col_center'})
upvote_links = answersdiv.find_all('a',attrs={'class':re.compile('main_button$')})
#answer_text = soup.body.find_all('div',attrs={'class':'ExpandedQText ExpandedAnswer'})

#store the upvote counts from all the answers
upvote_counts=[]
for link in upvote_links:
	span = link.find('span',attrs={'class':'count'})
	upvote_counts.append(span.text)

#store the view counts from all the answers
view_counts=[]
for view in views:
	view_counts.append(view.text)

#answer_chunks=[]
#for answer in answer_text:
#	ans_str=""
#	paras = answer.find_all('p',attrs={'class':'qtext_para'})
#	for p in paras:
#		ans_str = ans_str + p.text
#	answer_chunks.append(ans_str)

print 'upvotes: '+str(len(upvote_links))
#print 'answers: '+str(len(answers))
print 'views: '+str(len(views))

print upvote_counts
print view_counts

#converting the formattted numbers into integers
upvote_vals=[]
for u in upvote_counts:
	upvote_vals.append(format_num(u))

view_vals=[]
for v in view_counts:
	view_vals.append(format_num(v))

#reverse the list to show the data in reverse chronological order
upvote_vals.reverse()
view_vals.reverse()

print upvote_vals
print view_vals

print len(upvote_vals)
print len(view_vals)


#plot a bar graph with two rectangles
n_groups = len(upvote_vals)

fig,ax = plt.subplots()
#set logarithmic scale
ax.set_yscale('log')
index = np.arange(n_groups)
bar_width = 0.3

opacity = 0.6
error_config = {'ecolor':'0.3'}

rects1 = plt.bar(index, upvote_vals, bar_width,
		alpha=opacity,
		color='b',
		error_kw=error_config,
		label='Upvotes')

rects2 = plt.bar(index+bar_width,view_vals,bar_width,
		alpha=opacity,
		color='r',
		error_kw=error_config,
		label='Views')

plt.xlabel('Questions')
plt.ylabel('stats')
plt.title(' '.join(sys.argv[1]) + 'User Stats')
plt.tight_layout()
plt.legend()
plt.show()

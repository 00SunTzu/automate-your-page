# test data - example data for each scenario should be included
subtopica = "Lots of detail on the topic"
subtopicb = [1,["First Subtopic", "Details of First Subtopic"]]
subtopicc = [1,["Second Subtopic", "Details of Second Subtopic"]]
subtopicd = ["Introduction", subtopica, subtopicb, subtopicc, "Footnote"]

topicdetails1 = subtopica
topicdetails2 = subtopicb
topicdetails3 = subtopicc
topicdetails4 = subtopicd

topic1 = "First Topic"
topic2 = ["Second Topic", topicdetails1]
topic3 = ["Third Topic", topicdetails2]
topic4 = ["Fourth Topic", topicdetails3]
topic5 = ["Fifth Topic", topicdetails4]

lesson1topics = [topic1, topic2, topic3, topic3, topic4, topic5]
lesson2topics = [topic1, topic2, topic3]


lesson1 = ["First Lesson", lesson1topics]
lesson2 = ["Second Lesson", lesson2topics]
lesson3 = "Third Lesson"
lesson4 = ["Fourth Lesson", lesson2topics]
lesson5 = "Fifth Lesson"

project0lessons = [lesson1, lesson2]
project1lessons = [lesson1, lesson2, lesson3, lesson4, lesson5, "etc."]
project2lessons = [lesson3, lesson1]
							 
# -------------------------------------------------------------------
allprojects = ["Unknown Project",["Project 0", 0 ,project0lessons],["Project 1",2,project1lessons],["Project 3", 8, project2lessons]]                      
# -------------------------------------------------------------------
inputfile= ["Project2.css","UTF-8","Project 2 - Monique Dwyer","Introduction to Programming Nanodegree",allprojects]


def is_string(item):
	return str(type(item)) == "<type 'str'>"

def is_list(item):
	return str(type(item)) == "<type 'list'>"

def start_writing_my_webpage(cssfile, characterset, webpagename):
	return '''<!DOCTYPE HTML>
<html>
	<head>
		<meta charset="''' + characterset + '''">
		<title>''' + webpagename + '''</title>
		<link rel="stylesheet" type="text/css" href="''' + cssfile + '''">
	</head>
	<body>'''
	
def finish_writing_my_webpage():
	return'''
	</body>
</html>'''

def generate_TOC_entry(rectype, recordnum, listelement, llp):
	if listelement !="":
		if rectype == "topic":
			if is_string(listelement):
				topicName = listelement
			else:
				topicName = str(listelement[0])
			TOC_entry = '''
								<li><a href="#'''+ rectype + recordnum + '''">''' + topicName + '''</a></li>'''
		else:
			if rectype =="lesson":
				if is_string(listelement):
					lessonName = listelement
					TOC_entry = '''
						<li><a href="#'''+ rectype + recordnum + '''">''' + lessonName + '''</a></li> <!-- of Lesson Entry -->'''
				else:
					lessonName = str(listelement[0])
					TOC_entry = '''
						<li><a href="#'''+ rectype + recordnum + '''">''' + lessonName + '''</a>
							<ul>'''
			else:
				if is_string(listelement):
					projectName = listelement
					TOC_entry = '''
				<li>''' + projectName + '''</li>'''
				else:
					projectName = str(listelement[0])
					firstLesson = str(listelement[1])
					if firstLesson == "" :
						# find a default based on data to hand
						if llp == 0:
							firstLesson = "1"
						else:
							firstLesson = str(llp + 1)
					TOC_entry ='''
				<li>''' + projectName + '''
					<ol start="''' + firstLesson + '''">'''
	return TOC_entry

			
def generate_Content(entry):
	if is_string(entry):
		return generate_paragraph(entry)
	if is_list(entry):
		i = 0
		topicContent_HTML = ""
		# handle each item in the list
		while i < len(entry):
			if is_string(entry[i]):
				topicContent_HTML = topicContent_HTML + generate_paragraph(entry[i])
			if is_list(entry[i]):
				topicContent_HTML = topicContent_HTML + generate_list(entry[i])
				i = i + 1
		return topicContent_HTML
		
def generate_paragraph(entry):
	return '''
		<p>''' + entry + '''</p>'''

def generate_list(entry):
	if entry[0] == 1:
		return generate_subtopic(entry[1])
	if entry[0] == 2:
		return generate_unordered_list(entry[1])
	if entry[0] == 3:
		return generate_ordered_list(entry[1])
	if entry[0] == 4:
		return generate_detailed_list(entry[1])
			
def generate_detailed_list(entry):
	list_HTML = '''
		<dl>'''
	for e in entry:
		list_HTML = list_HTML + '''
			<dt>''' + e[0] + ''' + </dt>'''
		if is_string(e[1]) and e[1] != "":
			list_HTML = list_HTML + '''
				<dd>''' + e[1] + '''</dd>'''
		else:	
			x = 1
			while x < len(e[1]):
				list_HTML = list_HTML + '''
				<dd>''' + e[x] + '''</dd>'''
		list_HTML = list_HTML + '''
		</dl>'''
	return list_HTML

def generate_ordered_list(entry):
	list_HTML = '''
		<ol>'''
	for e in entry:
		if is_string(e):
			list_HTML = list_HTML + '''
			<li>''' + e + '''</li>'''
		if is_list(e):
			list_HTML = list_HTML + '''
			<li>''' + generate_list(e) + '''</li>'''
		list_HTML = list_HTML + '''
		</ol>'''
	return list_HTML
		
def generate_unordered_list(entry):
	list_HTML = '''
		<ul>'''
	for e in entry:
		if is_string(e):
			list_HTML = list_HTML + '''
			<li>''' + e + '''</li>'''
		if is_list(e):
			list_HTML = list_HTML + '''
			<li>''' + generate_list(e) + '''</li>'''
		list_HTML = list_HTML + '''
		</ul>'''
	return list_HTML
		
def generate_subtopic(entry):
	subtopic_HTML = '''
		<h4>''' + entry[0] + '''</h4>'''
	if is_string(entry[1]):
		return subtopic_HTML + generate_paragraph(entry[1])
	else:
		y = 0
		while y < len(entry[1]):
			if is_string(entry[y]):
				subtopic_HTML = subtopic_HTML + generate_paragraph(entry[y])
			else:
				subtopic_HTML = subtopic_HTML + generate_list(entry[y])
		return subtopic_HTML
			

def generate_Topic_entry(recordnum, listelement):
	if is_string(listelement):
		topicName = listelement
	else:
		topicName = str(listelement[0])
	return '''
				<div class="topic">
					<span><a id="topic'''  + recordnum + '''">''' + topicName + '''</a></span>'''

def generate_Lesson_entry(recordnum, listelement):
	if is_string(listelement):
		lessonName = listelement
	else:
		lessonName = str(listelement[0])
	return '''
			<div class="lesson">
				<h2><a id="lesson''' + recordnum + '''">''' + lessonName + '''</a></h2>'''
		
def process_Topic(type, recordnum, listelement):
	if type == "TOC":
		return generate_TOC_entry("topic", recordnum, listelement, 0)
	if type == "mainContent":
		return generate_Topic_entry(recordnum, listelement)
			
def process_Lesson(type, recordnum, listelement):
	if type == "TOC":
		return generate_TOC_entry("lesson", recordnum, listelement,0)
	if type == "mainContent":
		return generate_Lesson_entry(recordnum, listelement)

def process_Project(last_lesson_processed, listelement):
	return generate_TOC_entry("","",listelement,last_lesson_processed)
		
def generate_TOC_HTML(filedata):
	Projects = filedata[4]
	pcount = len(Projects)
	TOC_HTML = '''
		<div id="TOC">
			<h1 style="color: blue">''' + filedata[3] + '''</h1>
			<h1>Table of Content</h1>
			'''
	# Any Project information present?
	if pcount < 1:
		return TOC_HTML + '''
			
			NO PROJECT INFORMATION PROVIDED
			
			'''
	else:
		TOC_HTML = TOC_HTML + '''<ol type="I">'''	
		last_lesson_processed = 0
		for pelement in Projects:
			TOC_HTML = TOC_HTML + process_Project(last_lesson_processed, pelement)
				
			if not(is_string(pelement)):
				Lessons = pelement[2]
				
				if pelement[1] == "":
					lcount = last_lesson_processed + 1
				else:
					lcount = pelement[1]
				lnum = str(lcount)
				if len(Lessons) > 0:
					# Single entry string?
					if is_string(Lessons):
						if Lessons != "":
							TOC_HTML = TOC_HTML + process_Lesson("TOC", lnum, Lessons)
							lcount = lcount + 1
					else:
						for lelement in Lessons:
							# check Lesson data isn't just a string and whether it is empty'
							lnum = str(lcount)
							if is_string(lelement):
								if lelement != "":
									TOC_HTML = TOC_HTML + process_Lesson("TOC", lnum, lelement)
							else:
								TOC_HTML = TOC_HTML + process_Lesson("TOC", lnum, lelement)
								Topics = lelement[1]
								tcount = 1
								tnum = lnum + '''.''' + str(tcount)
								if len(Topics) > 0:
									# Single string Entry?
									if is_string(Topics):
										if Topics != "":
											TOC_HTML = TOC_HTML + process_Topic("TOC", tnum, Topics)
											tcount = tcount + 1
									else:
										for telement in Topics:
											tnum = lnum + '''.''' + str(tcount)
											# check Topic data isn't just a string and whether it is empty'
											if is_string(telement):
												if telement != "":
													TOC_HTML = TOC_HTML + process_Topic("TOC", tnum, telement)
													tcount = tcount + 1
											else:
												TOC_HTML = TOC_HTML + process_Topic("TOC", tnum, telement)
												tcount = tcount + 1
								if TOC_HTML [:-1][15:] != "Title Entry -->":
									TOC_HTML = TOC_HTML + '''
							</ul>
						</li> <!-- of Lesson Entry -->'''
							lcount = lcount + 1
				last_lesson_processed = lcount
				TOC_HTML = TOC_HTML + '''
					</ol>
				</li> <!-- of Project Entry -->'''
		return TOC_HTML + '''
			</ol> <!-- of TOC Table -->
		</div> <!-- of TOC -->'''
		
def generate_mainContent_HTML(filedata):#
	Projects = filedata[4]
	pcount = len(Projects)
	mainContent_HTML = '''
		<div class="mainContent">'''
	# Any Project information present?
	if is_string(Projects):
		return mainContent_HTML + '''
			
			NO PROJECT INFORMATION PROVIDED
			
			'''
	else:
		last_lesson_processed = 0
		for pelement in Projects:
			Lessons = pelement[2]
			if not(is_string(pelement)):
				if pelement[1] is None:
					lcount = last_lesson_processed + 1
					mainContent_HTML = mainContent_HTML + process_
				else:
					lcount = pelement[1]
				if len(Lessons) > 0:
					for lelement in Lessons:
						lnum = str(lcount)
						if is_string(lelement):
							if lelement != "":
								mainContent_HTML = mainContent_HTML + process_Lesson("mainContent", lnum, lelement)
						else:
							mainContent_HTML = mainContent_HTML + process_Lesson("mainContent", lnum, lelement)
							
							Topics = lelement[1]
							tcount = 1
						
							if len(Topics) > 0:
								if is_string(Topics):
									mainContent_HTML = mainContent_HTML + process_Topic("mainContent", lnum + '''.''' + str(tcount), Topics)
								else:									
									for telement in Topics:
										tnum = lnum + '''.''' + str(tcount)
										mainContent_HTML= mainContent_HTML + process_Topic("mainContent", tnum, telement) + '''
					<div class="topicContent">'''
										# I haven't got this working yet!!
										# mainContent_HTML= mainContent_HTML + generate_Content(telement)
										mainContent_HTML = mainContent_HTML + '''
					</div> <!-- of topicContent -->'''
										tcount = tcount + 1
										mainContent_HTML= mainContent_HTML + '''
				</div> <!-- of topic -->'''
						lcount = lcount + 1
						mainContent_HTML = mainContent_HTML + '''
			</div> <!-- of Lesson -->'''
		return mainContent_HTML + '''
		</div> <!-- of mainContent -->'''

def write_my_code(datafile):
	# check data format isvalid
	dcount = len(datafile)		
	if (dcount != 5) or not(is_string(datafile[0]) and is_string(datafile[1]) and is_string(datafile[2]) and is_string(datafile[3])):
		return 'Invalid/unexpected input - no code generated'
	# valid data file format	
	HTML_Output = start_writing_my_webpage(datafile[0],datafile[1],datafile[2])
	
	Projects = datafile[4]
	pcount = len(Projects)
	
	HTML_Output = HTML_Output + generate_TOC_HTML(datafile)
	HTML_Output = HTML_Output + generate_mainContent_HTML(datafile)
	HTML_Output = HTML_Output + finish_writing_my_webpage()
	return HTML_Output
	
print write_my_code(inputfile)



from .models import Vote, VoteResult
from django.db.models import Avg
import xml.etree.cElementTree as ET


def create_statistics_file(file, v):
    results = VoteResult.objects.filter(vote=v)
    res = VoteResult.objects.filter(vote=v).values(
        'subject__subjectName',
        'teacher__lName',
        'teacher__fName',
        'teacher__mName',
        'category__categoryName'
    ).annotate(
        average=Avg('value')
    )
    root = ET.Element("Statistics")
    for subj in res.values('subject__subjectName').distinct():
        sub = ET.SubElement(root, 'Subject', attrib={'Name': subj['subject__subjectName']})

        for teach in res.values('teacher__lName',
                                'teacher__fName',
                                'teacher__mName').filter(
            subject__subjectName=subj['subject__subjectName']).distinct():
            pers = ET.SubElement(sub, "Teacher", attrib={'Name': '{} {} {}'.format(teach['teacher__lName'],
                                                                                   teach['teacher__fName'],
                                                                                   teach['teacher__mName'])})

            for x, mark in enumerate(res.values('category_id',
                                                'category__categoryName',
                                                'average').filter(teacher__lName=teach['teacher__lName'],
                                                                  teacher__fName=teach['teacher__fName'],
                                                                  teacher__mName=teach['teacher__mName'],
                                                                  subject__subjectName=subj['subject__subjectName'])):
                ET.SubElement(pers,
                              'Category{}'.format(mark['category_id']),
                              Name=mark['category__categoryName']).text = str(round(mark['average'], 3))

    tree = ET.ElementTree(root)
    tree.write(file, encoding='utf-8')


def read_statistics_file(file):
    stats = {}
    tree = ET.parse(file)
    root = tree.getroot()
    # print(root.tag)
    for subject in root:
        # print(subject.tag, subject.attrib)
        for teacher in subject:
            # print(teacher.tag, teacher.attrib)
            for category in teacher:
                s = '{} - {}'.format(subject.attrib['Name'], teacher.attrib['Name'])
                if s in stats:
                    stats[s].append((category.attrib['Name'], category.text))
                else:
                    stats[s] = [(category.attrib['Name'], category.text)]

                # print(category.attrib, category.text)
                # print(category.getparent())

    # for key,value in stats.items():
        # for v in value:
        #     print(v)
        # print(key,value)
    return stats


from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_cat(tup, key):
    return tup[key]
from datetime import date 


class Citation:
    def __init__(self, author, master_title, year_of_publication):
        self.MONTH = [None, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


        self.author = author
        self.year_of_publication = year_of_publication 
        self.master_title = master_title
        self.access_date = self.get_date()

    @staticmethod
    def get_date():
        return date.today()

    def in_text(self):
        return '({author}, {year})'.format(author=self.master_title if self.author == None else self.author.get_intext_name(),year= 'n.d.' if self.year_of_publication == None else self.year_of_publication)
    

class Online(Citation):
    def __init__(self, author, year_of_publication, website_name, article_title, url):
        Citation.__init__(self, author, website_name, year_of_publication)
        self.website_name = website_name
        self.article_title = article_title
        self.url = url

class Website(Online):
    def __init__(self, author, year_of_publication, website_name, article_title, url):
        Online.__init__(self, author, year_of_publication, website_name, article_title, url)

    def end_text(self):
        part_one = self.website_name+'. ' if self.author==None else self.author.get_endtext_name() 
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = '{title}. '.format(title=self.article_title)
        part_four = '[Online] Available from:{url}. [Accessed:{date}].'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'))
        
        return part_one+part_two+part_three+part_four
    
    def in_text(self):
        return '({author}, {year})'.format(author=self.website_name if self.author == None else self.author.get_intext_name(),year= 'n.d.' if self.year_of_publication == None else self.year_of_publication)

class WebDocument(Website):
    def __init__(self, author, year_of_publication, month_of_publication, website_name ,article_title, url):
        Website.__init__(self, author, year_of_publication, website_name, article_title, url)
        self.month_of_publication = month_of_publication
    
    def end_text(self):
        part_one = self.website_name+'. ' if self.author==None else self.author.get_endtext_name() 
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = '{title}. '.format(title=self.article_title)
        part_four = '[Online] {month} {year}. Available from:{url}. [Accessed:{date}].'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'),month=self.MONTH[self.month_of_publication],year=self.year_of_publication)

        return part_one+part_two+part_three+part_four

class Journal(Citation):
    def __init__(self, author, year_of_publication, title_of_article, title_of_journal, volume_number, part_number, page):
        self.author = author
        self.year_of_publication = year_of_publication
        self.title_of_article = title_of_article
        self.title_of_journal = title_of_journal
        self.volume_number = volume_number
        self.part_number = part_number
        self.page = self.format_page_num(page) 

    

    def format_page_num(self, page):
        if isinstance(page,int):
            return '{}'.format(page)
        elif isinstance(page,tuple):
            if len(page) != 2:
                raise ValueError('Please insert a tuple of only TWO numbers')
            else :
                return '{start}-{to}'.format(start=page[0],to=page[1])
        else :
            raise ValueError('Only accept tuple or int type values')

    def end_text(self):
        part_one = '{name}'.format(name=self.author.get_endtext_name())
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = '{articletitle}. {journaltitle}. {vol} ({part}). p. {page}'.format(articletitle=self.title_of_article, journaltitle=self.title_of_journal, vol=self.volume_number, part=self.part_number, page=self.page)

        return part_one+part_two+part_three

    def in_text(self):
        return '({author}, {year})'.format(author=self.author.get_intext_name(source='journal'),year=self.year_of_publication)

class EJournal(Journal):
    def __init__(self, author, year_of_publication, title_of_article, title_of_journal, volume_number, part_number, page, url):
        Journal.__init__(self, author, year_of_publication, title_of_article, title_of_journal, volume_number, part_number, page)
        self.url = url

    def end_text(self):
        part_one = '{name}'.format(name=self.author.get_endtext_name())
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = '{articletitle}. {journaltitle}. {vol} ({part}). p. {page}.'.format(articletitle=self.title_of_article, journaltitle=self.title_of_journal, vol=self.volume_number, part=self.part_number, page=self.page)
        part_four = ' Available from:{url}. [Accessed: {date}]'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'))

        return part_one+part_two+part_three+part_four


class Names:
    '''
    Name objects to contain name(s) 
    of authors. 
    *names  -> Names(names)     variable amount of str
            -> Names([names])   list of names 
            -> Names((names))   tuple of names
    '''
    def __init__(self, *names):
        self.list_o_names = []
        if isinstance(names[0],list):
            self.list_o_names = names[0][:]
        elif isinstance(names[0],tuple):
            self.list_o_names = list(names[0])
        elif isinstance(names[0],str):
            self.list_o_names = list(names)
    
    def get_famname(self):
        '''
        Returns a list of strings containing 
        the family name in full.

        eg : ['Dickson', 'Trump', 'Perry']
        '''
        famnames = []
        for names in self.list_o_names:
            name = names.split(' ')
            famnames.append(name[-1])
        return famnames

    def get_givenname(self):
        '''
        Returns a list of strings containing 
        the given names in full. 

        eg : ['John Smith', 'Donald', 'Katy']
        '''
        givennames = []
        for names in self.list_o_names:
            name = names.split(' ')
            givennames.append(name[:-1])
        return givennames

    def get_initials(self):
        '''
        Returns a list of strings containing 
        the initials of the given names . 
        eg : ['J.S.', 'D.', 'K.']
        '''
        initials = []
        for givennames in self.get_givenname():
            # print(givennames)
            initial = ''
            if len(givennames)>1:
                # print('if')
                for every_name in givennames:
                    x = every_name[0]
                    initial += '{}.'.format(x)
                    # print(x)
            else:
                # print('else')
                for name in givennames:
                    x = name[0]
                    initial += '{}.'.format(x)
            initials.append(initial)
        return initials

    def get_endtext_name(self):
        '''
        Returns a string with names formatted 
        specifically to use in end-text citation.

        eg : Dickson, J.S. , Trump, D. and Perry, K.
        '''
        final = ''
        if len(self.get_famname()) == 1 :
            final += '{surname}, {initial} '.format(surname=self.get_famname()[0], initial=self.get_initials()[0])
        
        elif len(self.get_famname()) > 1:
            for i in range(len(self.get_famname())):
                final += '{surname}, {initial} '.format(surname=self.get_famname()[i], initial=self.get_initials()[i])
                if i < len(self.get_famname()) - 2  : 
                    final += ', '
                elif i == len(self.get_famname()) - 2 :
                    final += 'and '
                else:
                    pass
        return final

    def get_intext_name(self, source=None):
        '''
        Returns a string of family names
        formatted specifically for in-text citation.

        eg: Dickson, Trump and Perry
        '''
        if source == None:
            final = ''
            if len(self.get_famname()) == 1 :
                final += '{surname}'.format(surname=self.get_famname()[0])
            
            elif len(self.get_famname()) > 1:
                for i in range(len(self.get_famname())):
                    final += '{surname}'.format(surname=self.get_famname()[i])
                    if i < len(self.get_famname()) - 2  : 
                        final += ', '
                    elif i == len(self.get_famname()) - 2 :
                        final += ' and '
                    else:
                        pass
            return final
        
        elif source == 'journal':
            final = ''
            if len(self.get_famname()) == 1 :
                final += '{surname}'.format(surname=self.get_famname()[0])
            elif len(self.get_famname()) == 2:
                final += '{name1} and {name2}'.format(name1=self.get_famname()[0],name2=self.get_famname()[1])
            elif len(self.get_famname()) > 2:
                final += '{name1} et al.'.format(name1=self.get_famname()[0])
            return final



# a = Names('John Smith Jackson', 'Donald Trump','Hillary Clinton', 'Barrack Obama', 'Linus Sebastian', 'Tom Holland', 'Elon Musk')
# print(a.get_famname())
# a = Website('John', 'Smith', 2002, 'Facebook', 'How to listen to music', 'www.facebook.com')
# print(a.end_text())
# a = WebDocument(Names('John Smith Dickson','Elon Musk', 'Donald Trump','Katy Perry'), 2002, 1 ,'Facebook', 'How to listen to music', 'www.facebook.com')
# a = Website(None, None, 'Facebook', 'How to listen to music', 'www.facebook.com')
a = EJournal(Names(('Donald Trump', 'John Smith', 'Johnny English')), 2019,'How to use Twitter','Journal of Social Media', 1,7, (28,32),'https://journalonline.com')
# a = Citation(Names('Trump Donald'), 'Journal of nature', 2002)
print(a.in_text())


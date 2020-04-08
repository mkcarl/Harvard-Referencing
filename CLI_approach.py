from datetime import date 

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

    def __len__(self):
        return len(self.list_o_names)
    
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
        
        # return -> name et.al  
        elif source == 'journal':
            final = ''
            if len(self.get_famname()) == 1 :
                final += '{surname}'.format(surname=self.get_famname()[0])
            elif len(self.get_famname()) == 2:
                final += '{name1} and {name2}'.format(name1=self.get_famname()[0],name2=self.get_famname()[1])
            elif len(self.get_famname()) > 2:
                final += '{name1} et al.'.format(name1=self.get_famname()[0])
            return final


class Citation:
    '''
    General citation object. Shall not be used externally 

    Input : data types 

        author              -> Name object or None 
        master_title        -> str
        year_of_publication -> int
    '''
    def __init__(self, author, master_title, year_of_publication):
        self.MONTH = [None, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.author = author
        self.year_of_publication = self.format_year_of_publication(year_of_publication) 
        self.master_title = master_title
        self.access_date = self.get_date()

    def in_text(self):
            return '({author}, {year})'.format(author=self.master_title if self.author == None else self.author.get_intext_name(),year=self.year_of_publication)

    @staticmethod
    def get_date():
        return date.today()
   
    @staticmethod
    def position(number):
        '''
        Returns the ordinal of the int.  
        Example : 1st, 2nd

        input : data type
            number -> str or int 
        '''
        if isinstance(number,int):
            number = str(number)

        if number[-1] == 1 or number[-1] == '1':
            if number == 11 or number =='11':
                return '11th'
            else:
                return '{}st'.format(number)
        elif number[-1] == 2 or number[-1] == '2':
            if number == 12 or number =='12':
                return '12th'
            else:
                return '{}nd'.format(number)
        elif number[-1] == 3 or number[-1] == '3':
            if number == 13 or number =='13':
                return '13th'
            else:
                return '{}rd'.format(number)
        elif number[-1] == None or number[-1] == 'None': 
            return None 
        else:
            return '{}th'.format(number)

    @staticmethod
    def format_page_num(page):
        '''
        Return the page number in the format : 'from-to' / 'from'

        input : 
            page -> int or tuple with 2 elements only  
        '''
        if isinstance(page,int):
            return '{}'.format(page)
        elif isinstance(page,tuple):
            if len(page) != 2:
                raise ValueError('Please insert a tuple of only TWO numbers')
            else :
                return '{start}-{to}'.format(start=page[0],to=page[1])
        else :
            raise ValueError('Only accept tuple or int type values')
        
    @staticmethod
    def format_year_of_publication(year):
        if year == None : 
            return 'n.d.'
        else :
            return year
class Online(Citation):
    '''
    Citation for general online sources (with/without author(s)). 

    Format : 
            COMPANY/ORGANISATION/FAMILY/SURNAME, initials (if required) or name of 
            website if no author is available. (Year - in brackets) 
            Title of webpage – in italics or underlined. Any numbers if 
            website is part of a series – if needed. [Online –in square brackets] 
            Available from - URL. [Accessed: followed by date in square brackets]. 
    Input : data types 
            author               -> Name object or None
            year_of_publication  -> int
            website_name         -> str
            article_title        -> str
            url                  -> str
    '''
    def __init__(self, author, year_of_publication, website_name, article_title, url):
        Citation.__init__(self, author, website_name, year_of_publication)
        self.website_name = website_name
        self.article_title = article_title
        self.url = url

    def in_text(self):
        return '({author}, {year})'.format(author=self.website_name if self.author == None else self.author.get_intext_name(),year=self.year_of_publication)

    def end_text(self):
        part_one = self.website_name+'. ' if self.author==None else self.author.get_endtext_name() 
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = '{title}. '.format(title=self.article_title)
        part_four = '[Online] Available from:{url}. [Accessed:{date}].'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'))
        return part_one+part_two+part_three+part_four

class Website(Online):
    '''
    Citation for websites (with/without author(s)). 

    Format : 
            COMPANY/ORGANISATION/FAMILY/SURNAME, initials (if required) or name of 
            website if no author is available. (Year - in brackets) 
            Title of webpage – in italics or underlined. Any numbers if 
            website is part of a series – if needed. [Online –in square brackets] 
            Available from - URL. [Accessed: followed by date in square brackets]. 
    Input : data types 
            author               -> Name object or None
            year_of_publication  -> int
            website_name         -> str
            article_title        -> str
            url                  -> str
    '''
    pass

class Blog(Online):
    '''
    Citation for blogs (with/without author(s)). 

    Format : 
            COMPANY/ORGANISATION/FAMILY/SURNAME, initials (if required) or name of 
            website if no author is available. (Year - in brackets) 
            Title of webpage – in italics or underlined. Any numbers if 
            website is part of a series – if needed. [Online –in square brackets] 
            Available from - URL. [Accessed: followed by date in square brackets]. 
    Input : data types 
            author               -> Name object or None
            year_of_publication  -> int
            website_name         -> str
            blog_title           -> str
            url                  -> str
    '''
    def __init__(self, author, year_of_publication, website_name, blog_title, url):
        Online.__init__(self, author, year_of_publication, website_name, blog_title, url)

class WebDocument(Online):
    '''
    Citation for general online documents (with/without author(s)). 

    Format : 
            FAMILY/SURNAME, initials or name of website if no author is available. (Year - in brackets) 
            Title of web document – in italics or underlined. Any numbers as indicated on the web document, 
            i.e. if part of a series - if needed. [Online – in square brackets] Date of document – if specified. 
            Available from - URL. [Accessed: followed by date in square brackets] 
    Input : data types 
            author               -> Name object or None
            year_of_publication  -> int
            month_of_publication -> int
            website_name         -> str
            article_title        -> str
            url                  -> str
    '''
    def __init__(self, author, year_of_publication, month_of_publication, website_name ,article_title, url):
        Online.__init__(self, author, year_of_publication, website_name, article_title, url)
        self.month_of_publication = month_of_publication
    
    def end_text(self):
        part_one = self.website_name+'. ' if self.author==None else self.author.get_endtext_name() 
        part_two = '({year}) '.format(year=self.year_of_publication)
        part_three = '{title}. '.format(title=self.article_title)
        part_four = '[Online] {month} {year}. Available from:{url}. [Accessed:{date}].'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'),month=self.MONTH[self.month_of_publication],year=self.year_of_publication)

        return part_one+part_two+part_three+part_four

class Journal(Citation):
    '''
    Citation for journal articles (with author(s)). 

    Format : 
            FAMILY/SURNAME, Initials. (Year of publication – in brackets) Title of article. 
            Title of journal - in italics or underlined. Volume number. 
            (Part number/month – in brackets). p. followed by page 

 numbers. 
    Input : data types 
            author               -> Name object or None
            year_of_publication  -> int
            title_of_article     -> str
            title_of_journal     -> str
            volume_number        -> int 
            part_number          -> int 
            page                 -> None or int or tuple with 2 elements only
    '''
    def __init__(self, author, year_of_publication, title_of_article, title_of_journal, volume_number, part_number, page):
        Citation.__init__(self, author, title_of_journal, year_of_publication)
        self.title_of_article = title_of_article
        self.volume_number = volume_number
        self.part_number = part_number
        self.page = '' if page ==None else self.format_page_num(page) 

    def end_text(self):
        part_one = '{name}'.format(name=self.author.get_endtext_name())
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = '{articletitle}. {journaltitle}. {vol} ({part}). p. {page}'.format(articletitle=self.title_of_article, journaltitle=self.master_title, vol=self.volume_number, part=self.part_number, page=self.page)

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
        part_three = '{articletitle}. {journaltitle}. {vol} ({part}). p. {page}.'.format(articletitle=self.title_of_article, journaltitle=self.master_title, vol=self.volume_number, part=self.part_number, page=self.page)
        part_four = ' Available from:{url}. [Accessed: {date}]'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'))

        return part_one+part_two+part_three+part_four

class Book(Citation):
    '''
    Citation for books (with/without author(s)). 

    Format : 
            FAMILY/SURNAME, Initials. (Year of publication - in brackets) Title of chapter/contribution. 
            In: Author or Editor of Publication - Surname, Initials with (ed.) or (eds.) – in brackets, if relevant. 
            Book Title - in italics or underlined. Series title and volume - if available. 
            Edition - if not the first. Place of Publication: Publisher. 
    Input : data types 
            author               -> Name object or None
            book_title           -> str
            year_of_publication  -> int
            volume               -> int or None
            edition              -> int or None
            place_of_publication -> str
            publisher            -> str
    '''
    def __init__(self, author, book_title, year_of_publication, volume, edition, place_of_publication, publisher):
        Citation.__init__(self,author, book_title, year_of_publication)
        self.volume = str(volume) if volume != None else None
        self.edition = None if edition == None else self.position(str(edition))
        self.place_of_publication = place_of_publication
        self.publisher = publisher

    def end_text(self):
        part_one = '{name}({year}) '.format(name=self.author.get_endtext_name(),year=self.year_of_publication)
        part_two = '{booktitle}.'.format(booktitle=self.master_title)
        part_three = '{volume}'.format(volume= '' if self.volume==None else ' Volume ' + self.volume + '. ')
        part_four = '{edition}'.format(edition= '' if self.edition==None else ' ' + self.edition + ' edition. ' )
        part_five = '{place}: {publisher}.'.format(place=self.place_of_publication,publisher=self.publisher)

        return part_one+part_two+part_three+part_four+part_five

    def in_text(self):
        if len(self.author.list_o_names) < 4:
            return Citation.in_text(self)
        else : 
            return '({author}, {year})'.format(author=self.author.get_intext_name(source='journal'),year=self.year_of_publication) # return -> name et al.
        
class EBook(Book):
    '''
    Citation for books (with/without author(s)). 

    Format : 
            FAMILY/SURNAME, Initial(s). (Year of publication - in brackets) 
            Title - in italics or underlined. [Online – in square brackets] 
            City of publication: Publisher. Available from - URL. 
            [Accessed: followed by date in square brackets] 
    Input : data types 
            author               -> Name object or None
            book_title           -> str
            year_of_publication  -> int
            volume               -> int or None
            edition              -> int or None
            place_of_publication -> str
            publisher            -> str
            url                  -> str
        '''
    def __init__(self, author, book_title, year_of_publication, volume, edition, place_of_publication, publisher, url):
        Book.__init__(self, author, book_title, year_of_publication, volume, edition, place_of_publication, publisher)
        self.url = url

    def end_text(self):
        part_one = '{name}({year}) '.format(name=self.author.get_endtext_name(),year=self.year_of_publication)
        part_two = '{booktitle}. [Online]'.format(booktitle=self.master_title)
        part_three = '{volume}'.format(volume= '' if self.volume==None else ' Volume ' + self.volume + '. ')
        part_four = '{edition}'.format(edition= '' if self.edition==None else ' ' + self.edition + ' edition. ' )
        part_five = '{place}: {publisher}. '.format(place=self.place_of_publication,publisher=self.publisher)
        part_six = 'Available from:{url}. [Accessed: {date}]'.format(url=self.url, date=self.get_date().strftime('%d/%m/%Y'))

        return part_one+part_two+part_three+part_four+part_five+part_six

class Chapter(Book):
    '''
    Citation for particular chapter in a book by a specific author (with author(s)). 

    Format : 
            FAMILY/SURNAME, Initials. (Year of publication - in brackets) Title of chapter/contribution. 
            In: Author or Editor of Publication - Surname, Initials with (ed.) or (eds.) – in brackets, if relevant. 
            Book Title - in italics or underlined. Series title and volume - if available. Edition - if not the first. 
            Place of Publication: Publisher.
    Input : data types 
            author               -> Name object or None
            book_title           -> str
            editors              -> Name object or None
            year_of_publication  -> int
            volume               -> int or None
            edition              -> int or None
            place_of_publication -> str
            publisher            -> str
    '''
    def __init__(self, author, book_title, editors, year_of_publication, volume, edition, place_of_publication, publisher):
        Book.__init__(self, author, book_title, year_of_publication, volume, edition, place_of_publication, publisher)
        self.editors = editors
    
    def end_text(self):
        part_one = '{name}({year}) '.format(name=self.author.get_endtext_name(),year=self.year_of_publication)
        part_two = '{booktitle}. In: {editors} {amount}'.format(booktitle=self.master_title, editors=self.editors.get_endtext_name(), amount='(ed).' if len(self.editors) == 1 else '(eds).')
        part_three = '{volume}'.format(volume= '' if self.volume==None else ' Volume ' + self.volume + '. ')
        part_four = '{edition}'.format(edition= '' if self.edition==None else ' ' + self.edition + ' edition. ' )
        part_five = '{place}: {publisher}.'.format(place=self.place_of_publication,publisher=self.publisher)

        return part_one+part_two+part_three+part_four+part_five

    def in_text(self):
        if len(self.author.list_o_names) < 4:
            return Citation.in_text(self)
        else : 
            return '({author}, {year})'.format(author=self.author.get_intext_name(source='journal'),year=self.year_of_publication) # return -> name et al.

class Encyclopedia(Chapter):
    '''
    Citation for entry in an encyclopedia (with author(s)). 

    Format : 
            FAMILY/SURNAME, Initials. (Year of publication - in brackets) Title of chapter/contribution. 
            In: Author or Editor of Publication - Surname, Initials with (ed.) or (eds.) – in brackets, if relevant. 
            Book Title - in italics or underlined. Series title and volume - if available. Edition - if not the first. 
            Place of Publication: Publisher.
    Input : data types 
            author               -> Name object or None
            book_title           -> str
            editors              -> Name object or None
            year_of_publication  -> int
            volume               -> int or None
            edition              -> int or None
            place_of_publication -> str
            publisher            -> str
    '''
    pass

class Dictionary(Book):
    '''
    Citation for dictionaries (with/without author). 

    Format : 
            FAMILY/SURNAME, Initials. (ed.) or (eds.)-in brackets for editor(s) (Year of publication - in brackets) 
            Dictionary Title – in italics or underlined. Series title and/or volume - if available. 
            Edition - if not the first. Place of Publication: Publisher.
    Input : data types 
            author               -> Name object or None
            dictionary_title     -> str
            year_of_publication  -> int
            volume               -> int or None
            edition              -> int or None
            place_of_publication -> str
            publisher            -> str
    '''
    def __init__(self, author, dictionary_title, year_of_publication, volume, edition, place_of_publication, publisher):
        Book.__init__(self, author, dictionary_title, year_of_publication, volume, edition, place_of_publication, publisher)

    def end_text(self):
        part_one = '{name}{editor} ({year}) '.format(name=self.author.get_endtext_name() if self.author != None else self.master_title+'.',year=self.year_of_publication,editor='' if self.author == None else '(ed.) ' if len(self.author)==1 else '(eds.) ')
        part_two = '{booktitle}.'.format(booktitle=self.master_title)
        part_three = '{volume}'.format(volume= '' if self.volume==None else ' Volume ' + self.volume + '. ')
        part_four = '{edition}'.format(edition= '' if self.edition==None else ' ' + self.edition + ' edition. ' )
        part_five = '{place}: {publisher}.'.format(place=self.place_of_publication,publisher=self.publisher)

        return part_one+part_two+part_three+part_four+part_five

    def in_text(self):
        if self.author == None or len(self.author.list_o_names) < 4:
            return Citation.in_text(self)
        else : 
            return '({author}, {year})'.format(author=self.author.get_intext_name(source='journal'),year=self.year_of_publication)

class Image(Online):
    '''
    Citation for online images (with/without author). 

    Format : 
            FAMILY/SURNAME(S), Initials. (Year of publication) 
            Title or description of image - in italics or underlined. Name of organisation or website. 
            [Online Image] Available from - URL. [Accessed: followed by date].

    Input : data types 
            author               -> Name object or None
            year_of_publication  -> int
            website_name         -> str
            desc_of_img          -> str
            url                  -> str
    '''    
    def __init__(self, author, year_of_publication, website_name, desc_of_img, url):
        Online.__init__(self, author, year_of_publication, website_name, desc_of_img, url)

    def end_text(self):
        part_one = self.website_name+'. ' if self.author==None else self.author.get_endtext_name() 
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = '{title}. '.format(title=self.article_title)
        part_four = '[Online Image] Available from:{url}. [Accessed:{date}].'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'))
        return part_one+part_two+part_three+part_four

class Newspaper(Citation):
    '''
    Citation for newspaper articles (with/without author). 

    Format : 
            SURNAME, Initials. (Year of publication - in brackets) Title of Article.
            Title of Newspaper - in italics or underlined. Day and month of article. 
            Page number of article - if available.
    Input : data types 
            author               -> Name object or None
            newspaper_title      -> str
            year_of_publication  -> int
            article_title        -> str
            day_of_publication   -> int
            month_of_publication -> int
            page                 -> int or None
    '''
    def __init__(self, author, newspaper_title, year_of_publication, article_title, day_of_publication, month_of_publication, page):
        Citation.__init__(self, author, newspaper_title, year_of_publication)
        self.article_title = article_title
        self.day_of_publication = self.position(day_of_publication)
        self.month_of_publication = self.MONTH[month_of_publication]
        self.page = '' if page==None else  'p. ' +self.format_page_num(page)

    def end_text(self):
        part_one = '{name} '.format(name=self.master_title+'.' if self.author==None else self.author.get_endtext_name())
        part_two = '(n.d.) ' if self.year_of_publication==None else '({year}) '.format(year=self.year_of_publication)
        part_three = f'{self.article_title}. {self.master_title}. '
        part_four = f'{self.day_of_publication} {self.month_of_publication}.{self.page}'

        return part_one + part_two + part_three + part_four

class Video(WebDocument):
    '''
    Citation for videos online (with/without author(s)). 

    Format : 
            FAMILY/ SURNAME, initials or ORGANISATION IF NO NAMED PERSON IS AVAILABLE. (Year of distribution - in brackets) 
            Title of Online Video – in italics or underlined. If available indicate the Number and/or title if part of a series. 
            [Online video – in square brackets]. Date of the online video. Available from - URL. 
            [Accessed: followed by date in square brackets].
    Input : data types 
            author               -> Name object or None
            year_of_publication  -> int
            day_of_publication   -> int
            month_of_publication -> int
            website_name         -> str
            article_title        -> str
            url                  -> str
    '''
    def __init__(self, author, year_of_publication, day_of_publication, month_of_publication, channel_name ,video_title, url):
        WebDocument.__init__(self, author, year_of_publication, month_of_publication, channel_name ,video_title, url)
        self.day_of_publication = self.position(day_of_publication)

    def end_text(self):
        part_one = self.website_name+'. ' if self.author==None else self.author.get_endtext_name() 
        part_two = '({year}) '.format(year=self.year_of_publication)
        part_three = '{title}. '.format(title=self.article_title)
        part_four = '[Online Video] {day} {month}. Available from:{url}. [Accessed:{date}].'.format(url=self.url,date=self.get_date().strftime('%d/%m/%Y'),month=self.MONTH[self.month_of_publication],day=self.day_of_publication)

        return part_one+part_two+part_three+part_four

class Thesis(Citation):
    '''
    Citation for thesis 

    Format : 
        FAMILY/SURNAME, Initials. (Year of submission - in brackets) 
        Title of Thesis - in italics or underlined. Degree statement. 
        Degree Awarding Body. Location: Name of University. 

    Input : 
        author              -> Name object
        year_of_publication -> int
        thesis_title        -> str
        degree_statement    -> str
        degree_awarding_body-> str
        location            -> str
        university          -> str
    '''
    def __init__(self, author, year_of_publication, thesis_title, degree_statement, degree_awarding_body, location, university):
        Citation.__init__(self, author,thesis_title, year_of_publication)
        self.degree_statement = degree_statement
        self.degree_awarding_body = degree_awarding_body 
        self.location = location
        self.university = university

    def end_text(self):
        part_one = f'{self.author.get_endtext_name} ({self.year_of_publication}) '
        part_two = f'{self.master_title}. {self.degree_statement}. {self.degree_awarding_body}. '
        part_three = f'{self.location}: {self.university}'

        return part_one+part_two+part_three

        
if __name__ == '__main__':
    # a = Names('John Smith Jackson', 'Donald Trump','Hillary Clinton', 'Barrack Obama', 'Linus Sebastian', 'Tom Holland', 'Elon Musk')
    # print(a.get_famname())
    # a = Website(Names('John Legend', 'Smith Jackson'), 2002, 'Facebook', 'How to listen to music', 'www.facebook.com')
    # print(a.end_text())
    # a = WebDocument(Names('John Smith Dickson','Elon Musk', 'Donald Trump','Katy Perry'), 2002, 1 ,'Facebook', 'How to listen to music', 'www.facebook.com')
    # a = Website(None, None, 'Facebook', 'How to listen to music', 'www.facebook.com')
    # a = EJournal(Names(('Donald Trump', 'John Smith', 'Johnny English')), None,'How to use Twitter','Journal of Social Media', 1,7, (28,32),'https://journalonline.com')
    # a = Citation(Names('Trump Donald'), 'Journal of nature', 2002)
    # a = Dictionary(None,'Oxford Dictionary', 2001, 5, None, 'USA', 'Trump Ltd')
    # a = Chapter(Names('Donald Trump'),'how to be a president', Names('Hillary Clinton','Bill Clinton'), 2001, 5, None, 'USA', 'White House Ltd')
    a = Newspaper(None, 'The Star', None, 'What will happen during a global pandemic?', 25, 12, None)
    print(a.end_text())
    

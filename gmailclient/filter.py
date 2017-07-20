FILTER_DELIM = " OR "


class Filter:
    def __init__(self, fromAddr=set(), toAddr=set(), subject=set(), includes=set(), excludes=set()):
        self.fromAddr = fromAddr
        self.toAddr = toAddr
        self.subject = subject
        self.includes = includes
        self.excludes = excludes

    def __repr__(self):
        return str(self.__dict__)

    # from:(a@b.com) to:(c@d.com) subject:foo bar -zee
    # from - a@b.com, to - c@d.com, subject = foo, includes = foo, excludes = zee
    # more examples
    # from:(a@b.com) to:(c@d.com) subject:foo bar -{zee OR dee}
    @classmethod
    def fromFilterString(cls, filterStr=""):
        fromAddr = set()
        toAddr = set()
        subject = set()
        includes = set()
        excludes = set()

        if "from:" in filterStr:
            stringAfterFrom = filterStr[filterStr.index("from:") + len("from:") + 1:]
            allEmails = stringAfterFrom[:stringAfterFrom.index(")")]
            # fromStr = filterParts[1].split("+")[0].split("-")[0].replace("(", "").replace(")", "")
            fromAddr = set(allEmails.split(FILTER_DELIM))
        if "to:" in filterStr:
            stringAfterTo = filterStr[filterStr.index("to:") + len("to:") + 1:]
            allEmails = stringAfterTo[:stringAfterTo.index(")")]
            toAddr = set(allEmails.split(FILTER_DELIM))
        if "subject:" in filterStr:
            stringAfterSubject = filterStr[filterStr.index("subject:") + len("subject:"):]
            stringBeforeExcludes = stringAfterSubject.split("-")[0]
            if stringBeforeExcludes.startswith("("):
                allEmails = stringBeforeExcludes[1:stringBeforeExcludes.index(")") - 1]
                subject = set(allEmails.split(FILTER_DELIM))
            else:
                allEmails = stringBeforeExcludes.split(" ")[0]
                subject = set()
                subject.add(allEmails)
        if "-" in filterStr:
            stringAfterExclude = filterStr.split("-")[-1]
            print(stringAfterExclude)
            stringAfterExclude = stringAfterExclude.replace("{", "").replace("}", "")
            excludes = set(stringAfterExclude.split(FILTER_DELIM))
        return cls(fromAddr=fromAddr, toAddr=toAddr, excludes=excludes, includes=includes, subject=subject)

    # TODO: add case for toAddr, subjec and includes check. Currently just covers from and excludes
    def isMessageFiltered(self, message_dic):
        result = False
        # print(message_dic['subject'])
        if len(self.fromAddr) is not 0:
            # print(message_dic['fromEmail'])
            if message_dic['fromEmail'] in self.fromAddr or message_dic['fromEmail'].split('@')[1] in self.fromAddr:
                result = True
            else:
                return False
        # print("from:" + str(result))
        if len(self.toAddr) is not 0:
            if message_dic['to'] in self.toAddr:
                result = True
            else:
                return False
        # print("to:" + str(result))
        if len(self.subject) is not 0:
            mssgSubject = message_dic['subject']
            sub_result = False
            for mssg_substr in self.subject:
                if mssg_substr in mssgSubject:
                    sub_result = True
                    break
            if sub_result:
                result = True
            else:
                return False
        # print("subject:" + str(result))
        # do the opposite for excludes
        if len(self.excludes) is not 0:
            mssgSubject = message_dic['subject']
            sub_result = True
            for mssg_substr in self.excludes:
                if mssg_substr in mssgSubject:
                    sub_result = False
                    break
            if sub_result:
                result = True
            else:
                return False
        # print("excludes:" + str(result))
        return result


def main():
    c = Filter(toAddr=set())
    # or:
    # c = Filter.fromFilterString(filterStr="from:(a@b.com) to:(c@d.com) subject:foo bar -zee")
    # print(c)
    # d = Filter.fromFilterString(filterStr="from:(valueresearchonline.com OR editor@rakesh-jhunjhunwala.in OR safalniveshak.com OR rohitc99@indiatimes.com OR jagoinvestor.com OR dalal-street.in OR bemoneyaware@gmail.com OR trideep22280@gmail.com OR arunanalyst@rediffmail.com OR admin@microcapclub.com OR kapitall@kapitall.com OR capitalmind.in OR sptulsian.com OR jae.jun@oldschoolvalue.com OR noreply+feedproxy@google.com OR morningstar.com OR satyajeetmishra.com OR moodys.com OR forum.valuepickr.com OR wordpress.com OR valuewalk.com OR ukvalueinvestor.com OR capitalideasonline.com OR feedblitz.com OR sanasecurities.com OR blogtrottr.com OR analyseindia.com OR whitecoatinvestor.com OR thecalminvestor.com OR ritholtzwealth.com OR newsletter@abnormalreturns.com OR notify@sethgodin.com OR newsletter@farnamstreetblog.com OR newsletter@brainpickings.org OR fred@usv.com OR awealthofcommonsense@gmail.com OR shabbir@shabbir.in OR info@news.runtastic.com OR publishing@email.mckinsey.com OR stableinvestor@gmail.com OR hello@vipinkhandelwal.com OR mailvivek987@gmail.com OR macro@ycombinator.com OR support@zenhabits.net OR hackernewsletter.com OR startupdigestmail.com OR newsletter@brainpickings.org OR thereformedbroker.com OR mr1500@1500days.com OR newsletter@javacodegeeks.com OR ritholtzwealth.com OR interviewcake.com OR cambriainvestments.com OR smallcapvaluefind@gmail.com OR noreply@medium.com OR no_reply@ted.com OR subscribe@thefinancebuff.com) -{SaveMoneyIndia OR bimbima OR Quartz OR UrbanAsian OR Nanjappa OR newfanzoneblog OR Express OR Fortune OR OpIndia OR MoneyBeat OR Accommodation Times OR Confirm your subscription OR Green World Investor}")
    # print(d)


if __name__ == '__main__':
    main()

import csv
import time
from os import listdir
from os.path import isfile, join
inpath        = 'files/2017-03'
outpath       = 'files/out'

import os
os.system('cls' if os.name == 'nt' else 'clear')

# start with a dictionary of comma separated flags
# get the keys and make a new output dict


flags = {
  # flag            : tag
  'bike':           'Avantiplus'.split(','),
  'bills':          'YARRA VALLEY WTR,ORIGIN,OPTUS'.split(','),
  'car':            "CTX WOW,CALTEX,BURSON AUTOMOTIVE,VIC ROADS,BP WHITEHALL 5891,BBL 842 Sydney Rd,AUTO ONE,AMPOL REEDY CREEK,PEDDERS,VICROADS,PARTS 'R' US, RACV INSURANCE, car final".split(','),
  'cash':           'CUSS,ANZ FLINDERS,ATM,Cash,NAB LONSDALE,NAB 18-20 HOMER,NAB 658 HIGH'.split(','),
  'chemist':        'REHUB,SPECSAVERS MELB CENTRA   MELBOURNE   VIC,BRUNSWICK MEDICAL GR,CHEMIST,TEACHERS HEALTH'.split(','),
  'clothes':        "INDUSTRIE,GENERAL PANTS,FOSSIL,DANGERFIELD,COALITION BRANDS,CITY BEACH,ADIDAS,PINNACLE OUTDOORS,SUPER VILLAIN,Mr Simple".split(','),
  'credit':         '28 DEGREES MC,PAYMENT RECEIVED'.split(','),
  'fees':           'Debit Excess Int,ANNUAL FEE,Loan Repayment,AUTO PAYMENT,CBA CR CARD PMNT,Debit Excess Interest,Non CBA ATM Withdrawal Fee,CASH ADV,INTEREST CHARGES,Account Fee,Overdrawing Approval Fee'.split(','),
  'fines':          'VIC POL,ROBS AUTO ELEC'.split(','),
  'health':         'DISCOUNT DRUG STORE,BRUNSWICK CITY BATHS'.split(','),
  'hobbies':        'BCF AUSTRALIA,MUSICIANS PRO'.split(','),
  'pay':            'Credit Interest,CSEF Director Fee,Salary OUTWARE SYSTEMS,QMCODES USA INC, OUTWARE MOBILE MONTHLY PAYROLL,Conson Payment,HARPERCOLLINS'.split(','),
  'paypal':         'PAYPAL'.split(','),
  'pet':            'HERITAGE VETERINARY'.split(','),
  'rent':           'Transfer from LUKE WATTERS,DEFT'.split(','),
  'shopping':       'NORTHBRUN TATTS SUBNEW,SIMS SUPERMARKETS,IGA,FOODWORKS,FRIENDLY GROCER,BIG W,SAFEWAY,COLES,PIEDIMONTES,WOOLWORTHS'.split(','),
  'spending':       'FITZROY RAINBOW,COCA COLA AMATIL,CJ LUNCH BAR,CBD LONSDALE CONVENIEN,BRUNSWICK ARTS PROJE,BRUNETTI,BP BULLA,BD FED SQUARE,DA YUAN,AA CHURCH STREET 0274,303                      THCOT,3 SIBLINGS PTY LTD,2G ENTERPRISES PTY,SAVOY TAVERN,1000 POUND BEND,6 MARY STREET,7 ELEVEN,7 GRAMS,7-ELEVEN,Asian Beer Cafe,ASTRA BAR AND RESTAURA,AUSTRALIAN SEAFOOD,Baby Pizzeria,BAGUETTE FLINDERS,BANG BANG BOOGALOO,BARJAS PTY LTD,BEER BURGER,BLACK PEARL,BYRON BAY BEVERAGES,CAFE SHENKIN,CHERRY TREE,CLIQUE BAR,CLOUD NINE RESTAURAN,CORNER LANE CAFE,DAN MURPHYS,DASH TICKETS,DING DONG LOUNGE,DR CROFT,DRIFT CAFE,EARTHCORE,EB FREQ NASTY RUBIX,Edinburgh Castle,Elk Restaurant,EMERALD PEACOCK,EUREKA SKYDECK,EXETER CELLARS,EZYMART,FALLS CREEK SKI LIFT,FANCY HANKS,FLAGSTAFF CELLARS,GAMI CORP PTY LTD,GEORGE HOSPITALITY,GOLDEN MONKEY BAR,Good Beer Week,GRILLD,GRUMPYS GREEN,GUZMAN Y GOMEZ,HOLMES CONVIENIENCE,HOTEL,HOTHAM,HOTHAM ESTORE,HUNKY DORY,LA LA LAND,LAKSA BAR,LIQUORLAND,LOOP 23 PTY LTD,LYNDHURST DRIVE IN,MADAME BRUSSELS,MAI THAI,MASON DIXON SANDWICH,Mi Corazon,MR BURGER,NEW GOLD MOUNTAIN,Northcote Social Club,OXFORD SCHOLAR,PAPERBOY,PENNY BLACK,Railway H Brunswick,RIVERLAND BAR,SMALLBLOCK,SPACEAGEBACHELOR,SPICE KITCHEN,SPLEEN CENTRAL,STATE OF GRACE,SWISS AND CHIPS,TAHINI MELBOURNE VI,TANKERVILLE,THAT CHICKEN PLACE,THE GREAT BRITAIN,THE OLD BAR FITZROY,The Toff in Town,THINK ASIA MELBCENTR,TICKETEBO,TOUCHE HOMBRE,TOWN HALL PUB,TRUNK RESTAURANT,TRYBOOKING,TUSCAN BAR,Wesley Anne,WHOLE LOTTA LOVE,WIDJAJA,WORKERS FOOD ROOM,ZANZI BAR NEWTOWN,ZWIFT'.split(','),
  'tax':            'TAX OFFICE'.split(','),
  'taxable':        'Bunnings,DAYI ONLINESHOP,VIRGIN,WGI*SNAPNAMES.COM,JB HI FI,HERTZ,CRAZY DOMAINS,GUM.CO/CC THOUGHTBOT,DF PAINTBALL,MSY TECHNOLOGY,OFFICEWORKS,GITHUB,GOOGLE,HANDSETDETECTION,International Transaction,RACKSPACE,TWILIO,WORMLY,Amazon web,SKYPE,DIGITALOCEAN,INTNL TRANSACTION,HARVEST'.split(','),
  'taxi':           'CabFare,CABFARE,GM CABS,TAXI,UBER,SILVERTOP,INGOGO,BLACK CAB VIC'.split(','),
  'transfers':      'Refund Purchase, xx2489,xx1499,xx0699,xx2470,xx8119,NETBANK TRANSFER         PARRAMATTA'.split(','),
  'transport':      'MYKI, OPAL'.split(','),
  'travel':         'CARRY ON T2,BYRONSHIRE,JETSTAR,BP OZIGO,BP MT COTTON 4979,AGA TRAVEL INS,ALCTVM2'.split(','),

  # Direct Credit - payments from friends
  # holiday JETSTAR
  # linkme
}

# groups
# pay
outgoings = 'bills,bike,pet,health,car,cash,chemist,clothes,spending,fees,fines,paypal,rent,shopping,tax,taxable,taxi,transport'.split(',')
# taxable, transfers

# zero a dict of the tags
results = dict((t,0) for t in list(flags.keys()))
tags = {}
messages = []
unmatched_tags = []
duped = 0
spend = 0

bills         = 0
car           = 0
cashout       = 0
chemist       = 0
credit        = 0
entertainment = 0
fees          = 0
fines         = 0
offset        = 0
pay           = 0
paypal        = 0
rent          = 0
supermarket   = 0
tax           = 0
tax_payments  = 0
taxi          = 0
transfers     = 0
transport     = 0
unmatched     = 0
unmatched_amount = 0


csv.register_dialect(
  'mydialect',
  delimiter = ',',
  quotechar = '"',
  doublequote = True,
  skipinitialspace = True,
  lineterminator = '\r\n',
  quoting = csv.QUOTE_MINIMAL)

def openfile( file ):
  "Opens a file and returns a list of transactions"
  print 'Reading ' + inpath + '/' + file
  # TODO add try catch for CSV reading
  with open(inpath + '/' + file, 'rb') as f:
    reader = csv.reader(f)
    # like : ['06/10/2015', '-179.00', 'Transfer to xx8119 NetBank', '+0.20'],
    transactions = list(reader)
  return transactions

def writefile( file, transactions ):
  "Writes transactions to a csv file"
  print 'Writing tagged ' + outpath + '/' + file
  # TODO add try catch for output folder
  with open(outpath + '/' + file, 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    for transaction in transactions:
      thedatawriter.writerow(transaction)
  return;

# take nested dict and flip it so you can loop up the transaction and get a flag
def flip_flags( flags ):
  for flag, tag_list in flags.items():
    for tag in tag_list:
      tags[tag.strip().lower()] = flag.strip().lower()
  return tags;

def match_flags( flags, message ):
  for flag in flags:
    flag = flag.strip()
    tag = False
    if message.find(flag) > -1:
      tag = True
      break
  return tag;

def add_flags( transaction ):
  global duped
  global spend
  message = transaction[2].strip().lower()
  # transaction['tags'] = {}
  matched = False
  for tag, flag in tags.items():
    if message.find(tag) > -1:

      if matched != True:
        matched = True
        results[flag] += float(transaction[1])
        if flag in outgoings:
          spend += float(transaction[1])
      else: # if transaction[-2] != flag:
        print transaction[2] + ', flags: ' + transaction[-2] + ', ' + flag + ' - tags:  ' + transaction[-1] + ', ' + tag
        transaction.append('duped')
        duped += float(transaction[1])
      transaction.append(flag)
      transaction.append(tag)
  return matched



# =========================================

tags = flip_flags(flags)

files = [f for f in listdir(inpath) if isfile(join(inpath, f))]

for file in files:
  transactions = openfile( file )

  for transaction in transactions:
    transaction.append(file)

    trans_date = time.strptime(transaction[0], "%d/%m/%Y")
    transaction[0] = time.strftime("%Y-%m-%d", trans_date)

    if transaction[1][0] == '+':
      transaction[1] = transaction[1][1:]

    if not add_flags(transaction):
      unmatched += 1
      unmatched_amount -= float(transaction[1])
      unmatched_tags.append(transaction[2][0:30].strip())
      messages.append(transaction[1] + ' ' + transaction[2][0:100].strip().ljust(100) + ' ' + transaction[4])
      # print transaction[1] + ' ' +  transaction[2]

    # loop through our tags dict and see if any of the tags match our message
    # conflict = transaction[5] == transaction[7]
    # transaction.append(str(conflict))

  writefile(file, transactions)

# messages = sorted(set(messages))
# unmatched_tags = sorted(set(unmatched_tags))
# print 'Unmatched messages: ' + str(len(unmatched_tags))
# print "\n".join(messages)
print "\n".join(unmatched_tags)

print ""
print 'Pay = '            + str(pay)
print 'TODO linkme only pay = '
print 'Tax Offset = '     + str(offset)
print "add rent, bills and taxi to offset as a % "

print ""
print "Costs of debt: " + str(credit + fees + tax - transfers)
print "-------------"
print 'Credit Payments = '         + str(credit)
print 'Loan repayments, fees and charges= '           + str(fees)
print 'Tax Office Payments = '            + str(tax)
print 'Less transfers off credit = '      + str(transfers)
print "TODO separate into payments vs cash advances based on account"

print ""
print "Household: " + str(rent + bills)
print "-------------"
print 'Rent = '           + str(rent)
print 'Bills = '          + str(bills)

print ""
print "Costs of living : " + str(chemist + supermarket + transport)
print "-------------"
print 'Health and Chemist = '        + str(chemist)
print 'Supermarket = '    + str(supermarket)
print 'Transport / myki= '      + str(transport)

print ""
print "Discretionary : "  + str(cashout + entertainment + paypal + taxi)
print "-------------"
print 'Cash = '        + str(cashout)
print 'Entertainment = '  + str(entertainment)
print 'Paypal = '         + str(paypal)
print 'Taxi = '           + str(taxi)


print ""
print 'Fines = '          + str(fines)
print 'Car = '            + str(car)

print ""
print 'Unmatched: '      + str(unmatched)
print 'Unmatched amount: ' + str(unmatched_amount) + ' with an average of ' + str(unmatched_amount / unmatched)

print 'Auto matched tags: '
for k, v in results.items():
    print(k, v)


print 'outgoings = ' + str(spend)
print 'unaccounted = ' + str(results['pay'] + spend)

print 'duped = ' + str(duped)


print 'http://chargeprotect.com/ http://scamcharge.com for looking up charges'

print ""
print "TODO cli read dir name"
print "TODO add monthly in and out"
print "TODO add daily spend rates across categories"
print "TODO add html and chart output"
print "TODO move tags to DB"
print "TODO handle multiple bank statements - CBA, ING etc"
print "TODO auto download statements daily, run and email"
print "TODO auto suggest / lookup unmatched tags"

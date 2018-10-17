

def run():

    import pandas as pd
    # import matplotlib.pyplot as plt
    # import matplotlib.mlab as mlab
    import datetime as dt
    import pymatch.matching_functions as mf

    today = str(dt.datetime.today().date())

    print('---running')

    print('---preparing charity data')

    ch_reg      = mf.getData(['contact', 'geo', 'region'])
    ch_dist   = mf.getData(['contact', 'geo', 'admin_district'])
    ch_act      = mf.getData(['activities'])
    ch_name     = mf.getData(['name'])
    ch_ids      = mf.getData(['ids', 'GB-CHC'])
    ch_inc      = mf.getData(['income', 'latest', 'total'])
    ch_causes   = mf.getData(['causes'])
    # ch_pcode    = mf.getData(['contact', 'geo', 'postcode'], limit)
    ch_website  = mf.getData(['website'])

    print('total charities: ', len(ch_ids))

    print('---limiting to DK priority charities')

    # ------------------------------------------------------------------------------
    # extra formatting for causes, to create list of only charities DK are interested in

    # read in causes key and convert into dictionary
    ch_key = pd.read_csv('inputs/dkuk_cause_key.csv')

    # create dictionary of cause priorities from csv
    ch_key_dict = dict()
    for row in ch_key.itertuples():
        ch_key_dict[row.cause_id] = row.priority

    # set empty lists
    dk_priority, cause_ids, causes_all, keep_ids = [], [], [], []

    for i, charity in enumerate(ch_causes):

        ci = []
        ca = []
        dkp = 0
        dk_interest = True

        for c in charity:

            # store cause ids and names
            ci.append(c['id'])
            ca.append(c['name'])

            # check cause id against priority lookup and ignore if negative value
            if ch_key_dict[c['id']] == -1:
                dk_interest = False
                break

            if ch_key_dict[c['id']] == 1:
                dkp = 1

        # if cause lookup is positive or neutral store values
        if dk_interest:
            cause_ids.append(ci)
            causes_all.append(ca)
            dk_priority.append(dkp)
            keep_ids.append(ch_ids[i])

    # create table with all output data
    ch_cause_data = pd.DataFrame({'dk_priority':dk_priority,
                                    'cause_ids':cause_ids,
                                    'causes':causes_all}, index=keep_ids)

    print('number of remaining charities: ', len(ch_cause_data))


    # ------------------------------------------------------------------------------
    # FINAL DATA LOADING AND RESTRICTION

    print('---final data restriction')

    ch_all_data = pd.DataFrame({'name':ch_name,
                                'activities':ch_act,
                                'latest_income':ch_inc,
                                'region': ch_reg,
                                'district': ch_dist,
                                'website': ch_website}, index=ch_ids)

    ch_all_data.to_csv('ch_all_data_out.csv')

    # keep only charities with valid activities and income data, and latest income > £100k, this leaves 33,488 charities
    ch_valid_a = pd.DataFrame(ch_all_data[   (ch_all_data.activities.notnull())
                                            & (ch_all_data['latest_income'].notnull())
                                            & (ch_all_data['latest_income'] >= 100000)
                                            & (ch_all_data['latest_income'] <= 2000000)
                                          ])

    # merge with charities with relevant categories
    ch_valid = pd.DataFrame(ch_valid_a.merge(ch_cause_data, left_index=True, right_index=True))

    print('number of remaining charities: ', len(ch_valid))


    # ------------------------------------------------------------------------------
    # KEYWORD MATCHING

    print('---charity activity matching')
    print('---preparing input data')
    # input data

    # list of ids to use as reference in matching
    ch_valid_ids = ch_valid.index.values

    # process data before matching by stemming
    ch_act_stem = mf.word_stemmer(ch_valid['activities'].values)


    # keyword data

    # read in keywords file and convert to regex format
    ch_kw = pd.read_csv('inputs/tech_keywords_activity.csv')

    # keep only the terms which aren't flagged for removal
    ch_pos = ch_kw['positive'][ch_kw['remove'] != 1]
    ch_pos_terms = mf.regexer(mf.word_stemmer(ch_pos))

    ch_neg = ch_kw['negative'][ch_kw['remove'] != 1]
    ch_neg_terms = [mf.regexer(mf.word_stemmer(n.split(','))) if type(n) == str else [] for n in ch_neg]

    print('no. of match terms: ', len(ch_pos_terms))

    # run matching

    print('---running matching')

    ch_activity_matches = mf.keyword_match('activity', ch_act_stem,
                                            ch_pos_terms, ch_neg_terms, ch_valid_ids)

    print('number of matched charities: ', len(ch_activity_matches))


    # ------------------------------------------------------------------------------
    # GRANT DATA PREP

    print('---preparing grant data')

    # read in csv, only columns of interest, and parsing dates
    grants = pd.read_csv('inputs/grantnav.csv',

                         usecols=['Identifier', 'Title', 'Description', 'Amount Awarded',
                                  'Award Date', 'Planned Dates:Start Date', 'Recipient Org:Name',
                                  'Recipient Org:Charity Number', 'Funding Org:Identifier',
                                  'Funding Org:Name'],

                         parse_dates=['Award Date','Planned Dates:Start Date'])

    # limit to only grants with charity no. present and description
    grants = grants[(grants['Recipient Org:Charity Number'].notnull()) & (grants['Description'].notnull())]

    # limit to only rows where recipient charity id is valid number
    grants = grants[grants['Recipient Org:Charity Number'].apply(lambda x: x.isnumeric())]

    # turn charity no. field into integer
    grants['Recipient Org:Charity Number'] = grants['Recipient Org:Charity Number'].apply(lambda x: int(x))

    print('no. of grants:', len(grants))


    # ------------------------------------------------------------------------------
    # GRANT KEYWORD MATCHING

    print('---grant keyword matching')
    print('---preparing input data')

    # stem grants data
    gr_descs_stem = mf.word_stemmer(grants['Description'].values)


    # read in keywords file and convert to regex format
    gr_kw = pd.read_csv('inputs/tech_keywords_360.csv')

    # keep only the terms which aren't flagged for removal
    gr_pos = gr_kw['positive'][gr_kw['remove'] != 1]
    gr_pos_terms = mf.regexer(mf.word_stemmer(gr_pos))

    gr_neg = gr_kw['negative'][gr_kw['remove'] != 1]
    gr_neg_terms = [mf.regexer(mf.word_stemmer(n.split(','))) if type(n) == str else [] for n in gr_neg]

    print('no. of match terms: ', len(gr_pos_terms))

    # run matching_functions

    print('---running matching')

    gr_ids = grants['Identifier'].values

    gr_desc_matches = mf.keyword_match('grant', gr_descs_stem, gr_pos_terms, gr_neg_terms, gr_ids)

    print('number of grant matches: ', len(gr_desc_matches))


    # ------------------------------------------------------------------------------
    # OUTPUTS

    # CHARITY MATCH OUTPUTS

    ch_match_long = ch_activity_matches['activity_matched_words'].reset_index()

    # take only matched keywords, unstack from list and turn into long table with charity id and matched keywords
    ch_match_long = pd.DataFrame(ch_match_long.set_index('index').activity_matched_words.apply(pd.Series))
    ch_match_long = ch_match_long.stack().reset_index(level=-1, drop=True).astype(str).reset_index()
    ch_match_long.columns = ['id', 'activity_matched_words']
    ch_match_long.set_index('id', inplace = True)

    # join back on charity id to charity detail table
    ch_match_long_out = ch_match_long.merge(ch_valid, left_index=True, right_index=True)

    #output
    ch_match_long_out.to_csv('outputs/ch_activity_match_results_%s.csv' %today)

    ch_top_matches = ch_match_long.groupby(['activity_matched_words']).size().sort_values(ascending=True)
    # match_bar = ch_top_matches.plot.barh(figsize=(6,18))
    # match_bar.get_figure().savefig('OUTPUT_ch_activity_match_results_chart_%s.jpg' %today)


    # GRANT MATCH OUTPUTS

    # take only matched keywords, unstack from list and turn into long table with grant id and matched keywords
    gr_match_long = gr_desc_matches['grant_matched_words'].reset_index()
    gr_match_long = gr_match_long.set_index('index').grant_matched_words.apply(pd.Series).stack().reset_index(level=-1, drop=True).astype(str).reset_index()
    gr_match_long.columns = ['id', 'grant_matched_words']
    gr_match_long.set_index('id', inplace = True)

    # join back on id to grant detail table
    gr_match_long_out = gr_match_long.merge(grants, left_index=True, right_on='Identifier')

    # output
    gr_match_long_out.to_csv('outputs/gr_desc_match_results%s.csv' %today, index=false)

    ch_top_matches = gr_match_long.groupby(['grant_matched_words']).size().sort_values(ascending=True)
    # match_bar = ch_top_matches.plot.barh(figsize=(6,18))
    # match_bar.get_figure().savefig('OUTPUT_gr_desc_match_results_chart%s.jpg' %today)

    # ALL CHARITIES OUTPUTS

    # create flag fields in main table and join on match results for charities
    ch_valid['activity_keyword_match'] = ch_valid.index.isin(ch_activity_matches.index.values)
    ch_valid = ch_valid.merge(ch_activity_matches, how='left', left_index=True, right_index=True)

    # use the charity id field in grants table to flag matched grants
    ch_valid['grant_keyword_match'] = ch_valid.index.isin(gr_match_long_out['Recipient Org:Charity Number'])

    ch_valid['charity_id'] = ch_valid.index

    ch_valid.to_csv('outputs/all_charities_matched_%s.csv' %today, index=False)

    # final output is second copy of ch_valid for the dashboard
    ch_valid.to_csv('pydash/charity_input.csv', index=False)

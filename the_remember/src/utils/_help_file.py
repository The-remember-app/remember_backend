from the_remember.src.api.terms.dto import CreateTermAsTreeDTO

r_d = dict()
r_d |= {
    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>mean (</strong><strong>meant</strong><strong>, </strong><strong>meant</strong><strong>)</strong> &#8212; значить (иметь в виду)</li>
</ul>
<blockquote><p>What do you mean? – Что ты имеешь в виду?</p></blockquote>""": (
        "mean (meant, meant)", "", "значить (иметь в виду)", "<p>What do you mean? – Что ты имеешь в виду?</p>"),
    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>play</strong> – играть <strong>в </strong>игру или на муз. инструменте, воспроизводить видео\аудио</li>
</ul>
<blockquote><p>to play football – играть в футбол</p>
<p>to play guitar – играть на гитаре</p>
<p>Play the video again – Включите видео еще раз</p></blockquote>""": (
        "play", '', 'играть (в игру или на муз. инструменте, воспроизводить видео\аудио)', '''<p>to play football – играть в футбол</p>
<p>to play guitar – играть на гитаре</p>
<p>Play the video again – Включите видео еще раз</p>'''
    ),
    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>charge – </strong>обвинять (официально)</li>
</ul>
<blockquote><p>He has been charged with murder – Он обвинен в убийстве</p>
<p>He is charged with murdering his relative – Он обвиняется в убийстве родственника</p></blockquote>""":
        ("charge", "", "обвинять (официально)", """<p>He has been charged with murder – Он обвинен в убийстве</p>
<p>He is charged with murdering his relative – Он обвиняется в убийстве родственника</p>"""),

    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>perspective</strong> – перспектива (худож.), <strong>точка зрения, взляд</strong></li>
</ul>
<blockquote><p>He writes from a Marxist perspective – Он пишет с марксистской точки зрения</p></blockquote>""":
        ("perspective", "", "перспектива (худож.), точка зрения, взгляд",
         "<p>He writes from a Marxist perspective – Он пишет с марксистской точки зрения</p>"),

    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>design</strong> – дизайн, <strong>разработка</strong></li>
</ul>
<blockquote><p>I don’t like the design of this sofa – Мне не нравится дизайн этого дивана</p></blockquote>""":
        ("design", '', 'дизайн, разработка',
         "<p>I don’t like the design of this sofa – Мне не нравится дизайн этого дивана</p>"),
    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>advice</strong> – <strong>совет</strong>, советы</li>
</ul>
<blockquote><p>I took your advice. – Я последовал твоему совету (советам).</p>
<p>He gave me a piece of advice. – Он дал мне совет.</p></blockquote>""":
        ("advice", "", "совет", """<p>I took your advice. – Я последовал твоему совету (советам).</p>
<p>He gave me a piece of advice. – Он дал мне совет.</p>"""),
    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>court</strong> – <strong>(внутренний) </strong>двор, <strong>корт</strong></li>
</ul>
<blockquote><p>A court in the castle. – Внутренний двор замка.</p></blockquote>""":
        ("court", "", "(внутренний) двор, корт", "<p>A court in the castle. – Внутренний двор замка.</p>", ),
"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>flat</strong> (Br.) <strong>apartment</strong> (Am.) &#8212; квартира</li>
</ul>
<blockquote><p>I rent an apartment with my friends. – Я снимаю квартиру с друзьями.</p></blockquote>""":
    ("flat (Br.) apartment (Am.)", "", "квартира", "<p>I rent an apartment with my friends. – Я снимаю квартиру с друзьями.</p>", ),
"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>PC</strong><strong> (</strong><strong>personal</strong> <strong>computer</strong><strong>) </strong>– ПК, персональный компьютер</li>
</ul>
<blockquote><p>to upgrade a PC – усовершенствовать (апгрейдить) компьютер</p></blockquote>""":
("personal computer (PC)", "", "ПК, персональный компьютер", "<p>to upgrade a PC – усовершенствовать (апгрейдить) компьютер</p>", ),

"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>true</strong> – правдивый, <strong>настоящий</strong></li>
</ul>
<blockquote><p>true detective – настоящий детектив</p>
<p>What he is telling is true – То, что он говорит, &#8212; правда (правдиво)</p></blockquote>""":
("true", "", "правдивый, настоящий", """<p>true detective – настоящий детектив</p>
<p>What he is telling is true – То, что он говорит, &#8212; правда (правдиво)</p>""", ),
    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>weak</strong> &#8212; <strong>слабый</strong></li>
</ul>
<blockquote><p>weak link – слабое звено</p>
<p>weak muscles – слабые мышцы</p></blockquote>""": ("weak", "", "слабый", """<p>weak link – слабое звено</p>
<p>weak muscles – слабые мышцы</p>""",),
"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>conventional</strong> – обычный, <strong>традиционный</strong></li>
</ul>
<blockquote><p>Her views are remarkably conventional – Ее взгляды на удивление традиционны</p>
<p>conventional means of transportation – традиционные транспортные средства</p></blockquote>""":
    ("conventional", "", "обычный, традиционный", """<p>Her views are remarkably conventional – Ее взгляды на удивление традиционны</p>
<p>conventional means of transportation – традиционные транспортные средства</p>""", ),
"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>real</strong> – реальный, <strong>настоящий</strong></li>
</ul>
<blockquote><p>real hero – настоящий герой</p>
<p>real life – реальная жизнь</p></blockquote>""":
    ("real", "", "реальный, настоящий", """<p>real hero – настоящий герой</p>
<p>real life – реальная жизнь</p>""", ),
"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>national</strong> – национальный, <strong>государственный</strong></li>
</ul>
<blockquote><p>national anthem – государственный гимн</p>
<p>national security – национальная безопасность</p></blockquote>""":
    ("national", "", " национальный, государственный", """<p>national anthem – государственный гимн</p>
<p>national security – национальная безопасность</p>""", ),
"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>assistant</strong> – вспомогательный, <strong>помощник</strong></li>
</ul>
<blockquote><p>assistant manager – помощник менеджера</p></blockquote>""":
    ("assistant", "", "вспомогательный, помощник", """<p>assistant manager – помощник менеджера</p>""", ),
"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>remarkable</strong> – примечательный, <strong>выдающийся</strong></li>
</ul>
<blockquote><p>remarkable career – выдающаяся карьера</p>
<p>remarkable talent – выдающийся талант</p></blockquote>""":
    ("remarkable", "", "примечательный, выдающийся", """<p>remarkable career – выдающаяся карьера</p>
<p>remarkable talent – выдающийся талант</p>""", ),
    """<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>Простые союзы</strong> &#8212; состоят из одного слова</li>
</ul>
<blockquote><p>Nice <strong>and</strong> fluffy. &#8212; Милый <strong>и</strong> пушистый.</p>
<p>Small <strong>but</strong> proud. &#8212; Маленькая, <strong>но</strong> гордая.</p></blockquote>""":
        ("Простые союзы", "", "состоят из одного слова", """<p>Nice and fluffy. &#8212; Милый и пушистый.</p>
<p>Small but proud. &#8212; Маленькая, но гордая.</p>""",),
}

r_d |= {
    # Писать тут


}
'''
 """""": 
 ("", "", "", """""", ),
 
'''
r_d |= {"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>learning &#8212; </strong>изучение, процесс учебы</li>
</ul>
<blockquote><p>Apps make learning fun. – Приложения делают учебу интересной (веселой).</p></blockquote>""":
            ("learning", "", "изучение, процесс учебы",
             "<p>Apps make learning fun. – Приложения делают учебу интересной (веселой).</p>",),

"""<ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>mark (US), grade (UK)</strong> &#8212;<span style="text-decoration: line-through;">  </span>оценка, отметка</li>
</ul>
<blockquote><p>You have good marks (grades) in (for) English. – У тебя хорошие оценки по английскому.</p></blockquote>""":
        ("mark (US), grade (UK)", "", "оценка, отметка",
         "<p>You have good marks (grades) in (for) English. – У тебя хорошие оценки по английскому.</p>"),
        }

bad_terms = {
    "go on (went on, gone on)": "go on (went, gone)",
    "put off (put off, put off)": "put off (put, put)",
    "split (split, split)": "split",
    "throw (threw, thrown)": "throw (threw, torown)",  # FIXME
    "lie (lay, lain)": "lie (lay, lain)",
    "wear": "wear (wore, worn)",
    "de scribe": "describe",
    "compete (sport)": "compete",
    "be born (was, born)": "be born",
    "swear": "swear (swore, sworn)",
    "cut": "cut (cut, cut)",
    "ab sence": "absence",
    "stat e": "state",
    "will": 'will (power of will)',
    "lo ver": "lover",
    "workout, training": "workout training",
    "workout training": "workout, training",
    "terroris m": "terrorism",
    "military": "(the) military",
    "e nemy": "enemy",
    "manner": "manner (in that manner)",
    "tips": "tips (money)",
    "blo ck": "block",
    "priso ner": "prisoner",
    "i nternet": "internet",
    "pc (personal computer)": 'personal computer (pc)',
    "advanta ge": "advantage",
    "load cargo": "load, cargo"

}
bad_terms |= {v: k for k, v in bad_terms.items()}


def add_words(term, terms_entities):
    if term == 'alter':
        terms_entities["alter"] = CreateTermAsTreeDTO(term="alter",
                                                      definition="изменять, модицифировать что-то",
                                                      sub_sentences=[],
                                                      transcription=None)
    elif term == 'accuse':
        terms_entities["accuse"] = CreateTermAsTreeDTO(term="accuse", definition="обвинять",
                                                       sub_sentences=[],
                                                       transcription=None)
    elif term == 'charge':
        terms_entities["charge"] = CreateTermAsTreeDTO(term="charge", definition="обвинять (официально)",
                                                       sub_sentences=[],
                                                       transcription=None)
    elif term == 'suspect':
        terms_entities["suspect"] = CreateTermAsTreeDTO(term="suspect", definition="подозревать",
                                                        sub_sentences=[],
                                                        transcription=None)
    elif term == 'beat (up) (beat, beaten)':
        terms_entities["beat (up) (beat, beaten)"] = CreateTermAsTreeDTO(term="beat (up) (beat, beaten)",
                                                                         definition="бить, избивать",
                                                                         sub_sentences=[],
                                                                         transcription=None)
    elif term == 'murder':
        terms_entities["murder"] = CreateTermAsTreeDTO(term="murder", definition="убивать (новые слова)",
                                                       sub_sentences=[],
                                                       transcription=None)
    elif term == 'kill':
        terms_entities["kill"] = CreateTermAsTreeDTO(term="kill", definition="убивать",
                                                     sub_sentences=[],
                                                     transcription=None)
    elif term == 'attack':
        terms_entities["attack"] = CreateTermAsTreeDTO(term="attack", definition="нападать",
                                                       sub_sentences=[],
                                                       transcription=None)
    elif term == 'relationships':
        terms_entities["relationships"] = CreateTermAsTreeDTO(term="relationships", definition="отношения",
                                                              sub_sentences=[],
                                                              transcription=None)
    elif term == 'inmate':
        terms_entities["inmate"] = CreateTermAsTreeDTO(term="inmate", definition="заключенный",
                                                              sub_sentences=[],
                                                              transcription=None)
    elif term == 'guest':
        terms_entities["guest"] = CreateTermAsTreeDTO(term="guest", definition="гость",
                                                       sub_sentences=[],
                                                       transcription=None)

    elif term == 'простые союзы':
        terms_entities["простые союзы"] = CreateTermAsTreeDTO(term="simple unions", definition="простые союзы (состоят из одного слова)",
                                                       sub_sentences=[],
                                                       transcription=None)

MEMES = [
    {
        'pattern': '^(y u no) (.*)',
        'help': 'y u no {text}',
        'picture': 'http://memecaptain.com/y_u_no.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^aliens? guy (.+)',
        'help': 'aliens guy {text}',
        'picture': 'http://memecaptain.com/aliens.jpg',
        'groups': ['', 0]
    },
    {
        'pattern': '^((?:prepare|brace) (?:yourself|yourselves)) (.+)',
        'help': 'brace yourself {text}',
        'picture': 'http://i.imgur.com/cOnPlV7.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(.*) (all the .*)',
        'help': '{text} all the {things}',
        'picture': 'http://memecaptain.com/all_the_things.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(i don\'?t (?:always|normally) .*) (but when i do,? .*)',
        'help': 'I don\'t always {something} but when I do {text}',
        'picture': 'http://memecaptain.com/most_interesting.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(.*)(\stoo damn .*)',
        'help': '{text} too damn {something}',
        'picture': 'http://memecaptain.com/too_damn_high.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(not sure if .*) (or .*)',
        'help': 'not sure if {something} or {something else}',
        'picture': 'http://memecaptain.com/fry.png',
        'groups': [0, 1]
    },
    {
        'pattern': '^(yo dawg .*) (so .*)',
        'help': 'yo dawg {text} so {text}',
        'picture': 'http://memecaptain.com/xzibit.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(all your .*) (are belong to .*)',
        'help': 'all your {text} are belong to {text}',
        'picture': 'http://i.imgur.com/gzPiQ8R.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(one does not simply) (.*)',
        'help': 'one does not simply {text}',
        'picture': 'http://memecaptain.com/boromir.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(if you .*\s)(.* gonna have a bad time)',
        'help': 'if you {text} gonna have a bad time',
        'picture': 'http://memecaptain.com/bad_time.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(if .*), ((?:are|can|do|does|how|is|may|might|should|then|what|when|where|which|who|why|will|won\'t|would) .*)',
        'help': 'if {text}, {word that can start a question} {text}?',
        'picture': 'http://memecaptain.com/philosoraptor.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^((?:how|what|when|where|who|why) the (?:hell|heck|fuck|shit|crap|damn)) (.*)',
        'help': '{word that can start a question} the {expletive} {text}',
        'picture': 'http://memecaptain.com/src_images/z8IPtw',
        'groups': [0, 1]
    },
    {
        'pattern': '^(?:success|nailed it) when (.*) then (.*)',
        'help': 'success when {text} then {text}',
        'picture': 'http://memecaptain.com/success_kid.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(?:fwp|cry) when (.*) then (.*)',
        'help': 'cry when {text} then {text}',
        'picture': 'http://v1.memecaptain.com/first_world_problems.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^bad luck when (.*) then (.*)',
        'help': 'bad luck when {text} then {text}',
        'picture': 'http://v1.memecaptain.com/bad_luck_brian.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^scumbag(?: steve)? (.*) then (.*)',
        'help': 'scumbag {text} then {text}',
        'picture': 'http://v1.memecaptain.com/scumbag_steve.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(what if i told you) (.+)',
        'help': 'what if I told you {text}',
        'picture': 'http://memecaptain.com/src_images/fWle1w',
        'groups': [0, 1]
    },
    {
        'pattern': '^(i hate) (.+)',
        'help': 'I hate {text}',
        'picture': 'http://memecaptain.com/src_images/_k6JVg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(why can\'?t (?:i|we|you|he|she|it|they)) (.+)',
        'help': 'why can\'t {personal pronoun} {text}',
        'picture': 'http://i0.kym-cdn.com/photos/images/newsfeed/000/075/683/limes_guy.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(.+),? (how (?:do (?:they|I)|does (?:he|she|it)) work\??)',
        'help': '{things}, how do they work?',
        'picture': 'http://i2.kym-cdn.com/photos/images/original/000/046/123/magnets.jpg',
        'groups': [0, 1]
    },
    {
        'pattern': '^(.+?(?:a{3,}|e{3,}|i{3,}|o{3,}|u{3,}|y{3,}).*)',
        'help': '{text}{3 x a|e|i|o|u|y}{text}',
        'picture': 'http://memecaptain.com/src_images/L50mqA',
        'groups': [0, 1]
    },
]

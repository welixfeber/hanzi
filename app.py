"""
========================================================================
 Hanzi Explorer — character-decomposition learning app
 Single-file Streamlit app.  Deploy free on Streamlit Cloud / HF Spaces.

 Files needed in your repo:
   app.py            <- this file
   requirements.txt  <- contains:  streamlit
                                    hanzipy
========================================================================
"""
import streamlit as st

# hanzipy is pure-python + bundles CC-CEDICT & cjkvi-ids data, so it
# works on any free host with no external API / internet needed.
from hanzipy.dictionary import HanziDictionary
from hanzipy.decomposer import HanziDecomposer

# ----------------------------------------------------------------------
# 214 KANGXI RADICAL DICTIONARY  (canonical meaning + pinyin + variants)
# ----------------------------------------------------------------------
KANGXI = {
1:("一","yī","one",[]),2:("丨","gǔn","line",[]),3:("丶","zhǔ","dot",[]),
4:("丿","piě","slash",["乀","乁"]),5:("乙","yǐ","second",["乚","乛","⺄"]),
6:("亅","jué","hook",[]),7:("二","èr","two",[]),8:("亠","tóu","lid",[]),
9:("人","rén","person",["亻","𠆢"]),10:("儿","ér","legs",[]),11:("入","rù","enter",[]),
12:("八","bā","eight",[]),13:("冂","jiōng","down box",[]),14:("冖","mì","cover",[]),
15:("冫","bīng","ice",[]),16:("几","jī","table",[]),17:("凵","qū","open box",[]),
18:("刀","dāo","knife",["刂"]),19:("力","lì","power",[]),20:("勹","bāo","wrap",[]),
21:("匕","bǐ","spoon",[]),22:("匚","fāng","right open box",[]),23:("匸","xǐ","hiding enclosure",[]),
24:("十","shí","ten",[]),25:("卜","bǔ","divination",[]),26:("卩","jié","seal",["㔾"]),
27:("厂","hàn","cliff",[]),28:("厶","sī","private",[]),29:("又","yòu","again",[]),
30:("口","kǒu","mouth",[]),31:("囗","wéi","enclosure",[]),32:("土","tǔ","earth",[]),
33:("士","shì","scholar",[]),34:("夂","zhǐ","go",[]),35:("夊","suī","go slowly",[]),
36:("夕","xī","evening",[]),37:("大","dà","big",[]),38:("女","nǚ","woman",[]),
39:("子","zǐ","child",[]),40:("宀","mián","roof",[]),41:("寸","cùn","inch",[]),
42:("小","xiǎo","small",["⺌","⺍"]),43:("尢","wāng","lame",["尣"]),44:("尸","shī","corpse",[]),
45:("屮","chè","sprout",[]),46:("山","shān","mountain",[]),47:("巛","chuān","river",["川","巜"]),
48:("工","gōng","work",[]),49:("己","jǐ","oneself",[]),50:("巾","jīn","turban",[]),
51:("干","gān","dry",[]),52:("幺","yāo","short thread",[]),53:("广","guǎng","dotted cliff",[]),
54:("廴","yǐn","long stride",[]),55:("廾","gǒng","two hands",[]),56:("弋","yì","shoot",[]),
57:("弓","gōng","bow",[]),58:("彐","jì","snout",["彑"]),59:("彡","shān","bristle",[]),
60:("彳","chì","step",[]),61:("心","xīn","heart",["忄","⺗"]),62:("戈","gē","halberd",[]),
63:("戶","hù","door",["户","戸"]),64:("手","shǒu","hand",["扌","龵"]),65:("支","zhī","branch",[]),
66:("攴","pū","rap",["攵"]),67:("文","wén","script",[]),68:("斗","dǒu","dipper",[]),
69:("斤","jīn","axe",[]),70:("方","fāng","square",[]),71:("无","wú","not",["旡"]),
72:("日","rì","sun",[]),73:("曰","yuē","say",[]),74:("月","yuè","moon",[]),
75:("木","mù","tree",[]),76:("欠","qiàn","lack",[]),77:("止","zhǐ","stop",[]),
78:("歹","dǎi","death",["歺"]),79:("殳","shū","weapon",[]),80:("毋","wú","do not",["母","⺟"]),
81:("比","bǐ","compare",[]),82:("毛","máo","fur",[]),83:("氏","shì","clan",[]),
84:("气","qì","steam",[]),85:("水","shuǐ","water",["氺","氵"]),86:("火","huǒ","fire",["灬"]),
87:("爪","zhǎo","claw",["爫"]),88:("父","fù","father",[]),89:("爻","yáo","double x",[]),
90:("爿","qiáng","half tree trunk",["丬"]),91:("片","piàn","slice",[]),92:("牙","yá","fang",[]),
93:("牛","niú","cow",["牜","⺧"]),94:("犬","quǎn","dog",["犭"]),95:("玄","xuán","profound",[]),
96:("玉","yù","jade",["王","玊","⺩"]),97:("瓜","guā","melon",[]),98:("瓦","wǎ","tile",[]),
99:("甘","gān","sweet",[]),100:("生","shēng","life",[]),101:("用","yòng","use",[]),
102:("田","tián","field",[]),103:("疋","pǐ","bolt of cloth",["⺪"]),104:("疒","nè","sickness",[]),
105:("癶","bō","dotted tent",[]),106:("白","bái","white",[]),107:("皮","pí","skin",[]),
108:("皿","mǐn","dish",[]),109:("目","mù","eye",[]),110:("矛","máo","spear",[]),
111:("矢","shǐ","arrow",[]),112:("石","shí","stone",[]),113:("示","shì","spirit",["礻"]),
114:("禸","róu","track",[]),115:("禾","hé","grain",[]),116:("穴","xué","cave",[]),
117:("立","lì","stand",[]),118:("竹","zhú","bamboo",["⺮"]),119:("米","mǐ","rice",[]),
120:("糸","mì","silk",["糹","纟"]),121:("缶","fǒu","jar",[]),122:("网","wǎng","net",["罒","⺲","罓","⺳"]),
123:("羊","yáng","sheep",["⺶","⺷"]),124:("羽","yǔ","feather",[]),125:("老","lǎo","old",["耂"]),
126:("而","ér","and",[]),127:("耒","lěi","plow",[]),128:("耳","ěr","ear",[]),
129:("聿","yù","brush",["⺻"]),130:("肉","ròu","meat",["⺼"]),131:("臣","chén","minister",[]),
132:("自","zì","self",[]),133:("至","zhì","arrive",[]),134:("臼","jiù","mortar",[]),
135:("舌","shé","tongue",[]),136:("舛","chuǎn","oppose",[]),137:("舟","zhōu","boat",[]),
138:("艮","gèn","stopping",[]),139:("色","sè","color",[]),140:("艸","cǎo","grass",["艹"]),
141:("虍","hū","tiger",[]),142:("虫","chóng","insect",[]),143:("血","xuè","blood",[]),
144:("行","xíng","walk",[]),145:("衣","yī","clothes",["衤"]),146:("襾","yà","cover",["西","覀"]),
147:("見","jiàn","see",["见"]),148:("角","jiǎo","horn",[]),149:("言","yán","speech",["訁","讠"]),
150:("谷","gǔ","valley",[]),151:("豆","dòu","bean",[]),152:("豕","shǐ","pig",[]),
153:("豸","zhì","badger",[]),154:("貝","bèi","shell",["贝"]),155:("赤","chì","red",[]),
156:("走","zǒu","run",["赱"]),157:("足","zú","foot",["⻊"]),158:("身","shēn","body",[]),
159:("車","chē","cart",["车"]),160:("辛","xīn","bitter",[]),161:("辰","chén","morning",[]),
162:("辵","chuò","walk",["辶","⻌","⻍"]),163:("邑","yì","city",["阝","⻏","⻖"]),164:("酉","yǒu","wine",[]),
165:("釆","biàn","distinguish",[]),166:("里","lǐ","village",[]),167:("金","jīn","gold",["釒","钅"]),
168:("長","cháng","long",["镸","长"]),169:("門","mén","gate",["门"]),170:("阜","fù","mound",["阝"]),
171:("隶","lì","slave",[]),172:("隹","zhuī","short-tailed bird",[]),173:("雨","yǔ","rain",[]),
174:("青","qīng","blue",["靑"]),175:("非","fēi","wrong",[]),176:("面","miàn","face",["靣"]),
177:("革","gé","leather",[]),178:("韋","wéi","tanned leather",["韦"]),179:("韭","jiǔ","leek",[]),
180:("音","yīn","sound",[]),181:("頁","yè","leaf/page",["页"]),182:("風","fēng","wind",["风"]),
183:("飛","fēi","fly",["飞"]),184:("食","shí","eat",["飠","饣"]),185:("首","shǒu","head",[]),
186:("香","xiāng","fragrant",[]),187:("馬","mǎ","horse",["马"]),188:("骨","gǔ","bone",[]),
189:("高","gāo","tall",["髙"]),190:("髟","biāo","hair",[]),191:("鬥","dòu","fight",[]),
192:("鬯","chàng","sacrificial wine",[]),193:("鬲","lì","cauldron",[]),194:("鬼","guǐ","ghost",[]),
195:("魚","yú","fish",["鱼"]),196:("鳥","niǎo","bird",["鸟"]),197:("鹵","lǔ","salt",["卤"]),
198:("鹿","lù","deer",[]),199:("麥","mài","wheat",["麦"]),200:("麻","má","hemp",[]),
201:("黃","huáng","yellow",["黄"]),202:("黍","shǔ","millet",[]),203:("黑","hēi","black",[]),
204:("黹","zhǐ","embroidery",[]),205:("黽","mǐn","frog",["黾"]),206:("鼎","dǐng","tripod",[]),
207:("鼓","gǔ","drum",[]),208:("鼠","shǔ","rat",[]),209:("鼻","bí","nose",[]),
210:("齊","qí","even",["齐"]),211:("齒","chǐ","tooth",["齿"]),212:("龍","lóng","dragon",["龙"]),
213:("龜","guī","turtle",["龟"]),214:("龠","yuè","flute",[]),
}

def _build_radical_lookup():
    lookup = {}
    for num,(glyph,pinyin,meaning,variants) in KANGXI.items():
        rec = {"radical_number":num,"canonical":glyph,"pinyin":pinyin,"meaning":meaning}
        lookup[glyph] = rec
        for v in variants:
            lookup[v] = {**rec,"variant_form":v}
    return lookup

RADICAL_LOOKUP = _build_radical_lookup()

# ----------------------------------------------------------------------
# ENGINE
# ----------------------------------------------------------------------
class ChineseCharacterEngine:
    def __init__(self, radical_lookup):
        self._dict = HanziDictionary()
        self._decomposer = HanziDecomposer()
        self._radicals = radical_lookup
        self._comp_cache = {}

    def _is_chinese(self, ch):
        cp = ord(ch)
        return 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF

    def _lookup(self, item):
        try:
            entries = self._dict.definition_lookup(item)
        except Exception:
            return []
        return [{"pinyin":e.get("pinyin",""),"meaning":e.get("definition","")} for e in entries]

    def _component_info(self, comp):
        if comp in self._comp_cache:
            return self._comp_cache[comp]
        rad = self._radicals.get(comp)
        if rad:
            info = {"component":comp,"meaning":rad["meaning"],"pinyin":rad["pinyin"],
                    "radical_number":rad["radical_number"],"source":"kangxi"}
            if "variant_form" in rad:
                info["note"] = f"variant of {rad['canonical']}"
        else:
            defs = self._lookup(comp)
            info = ({"component":comp,"meaning":defs[0]["meaning"].split("/")[0],
                     "pinyin":defs[0]["pinyin"],"source":"cedict"} if defs else
                    {"component":comp,"meaning":"(structural component)","pinyin":"","source":"unknown"})
        self._comp_cache[comp] = info
        return info

    def _components(self, ch):
        try:
            decomp = self._decomposer.decompose(ch)
        except Exception:
            return []
        seen, out = set(), []
        for c in decomp.get("radical", []) or []:
            if c == ch or c in seen or not c.strip():
                continue
            seen.add(c)
            out.append(self._component_info(c))
        return out

    def _examples(self, ch, limit=6):
        try:
            ex = self._dict.get_examples(ch)
        except Exception:
            return []
        words = []
        for tier in ("high_frequency","mid_frequency","low_frequency"):
            for w in ex.get(tier, []):
                if w.get("simplified") == ch:
                    continue
                words.append({"word":w.get("simplified",""),"pinyin":w.get("pinyin",""),
                              "meaning":w.get("definition",""),"frequency":tier.replace("_frequency","")})
                if len(words) >= limit:
                    return words
        return words

    def explain_character(self, ch):
        return {"character":ch,"readings":self._lookup(ch),
                "components":self._components(ch),"appears_in":self._examples(ch)}

    def explain_phrase(self, phrase):
        self._comp_cache = {}
        try:
            words = self._dict.segment(phrase)
        except Exception:
            words = list(phrase)
        word_objs = []
        for w in words:
            if not any(self._is_chinese(c) for c in w):
                continue
            word_objs.append({"word":w,"readings":self._lookup(w),
                              "characters":[self.explain_character(c) for c in w if self._is_chinese(c)]})
        return {"input":phrase,"language":"zh","words":word_objs}

# ----------------------------------------------------------------------
# STREAMLIT UI
# ----------------------------------------------------------------------
@st.cache_resource
def get_engine():
    return ChineseCharacterEngine(RADICAL_LOOKUP)

st.set_page_config(page_title="Hanzi Explorer", page_icon="🀄", layout="centered")
st.title("🀄 Hanzi Explorer")
st.caption("Paste a Chinese word or phrase → see every character broken into its building blocks.")

engine = get_engine()

phrase = st.text_input("Enter Chinese text", value="电影院",
                       placeholder="e.g. 电影院, 医院, 我想去中国")

if phrase.strip():
    result = engine.explain_phrase(phrase)
    if not result["words"]:
        st.warning("No Chinese characters found. Try pasting some 汉字.")
    for w in result["words"]:
        word_reading = w["readings"][0] if w["readings"] else None
        header = f"### {w['word']}"
        if word_reading:
            header += f"  —  *{word_reading['pinyin']}*"
        st.markdown(header)
        if word_reading:
            st.markdown(f"**Meaning:** {word_reading['meaning']}")

        for c in w["characters"]:
            rd = c["readings"][0] if c["readings"] else {"pinyin":"?","meaning":"?"}
            with st.expander(f"🔹 {c['character']}  [{rd['pinyin']}]  —  {rd['meaning'][:40]}", expanded=True):
                st.markdown(f"**{c['character']}** · *{rd['pinyin']}* — {rd['meaning']}")

                if c["components"]:
                    st.markdown("**Building blocks (components):**")
                    for comp in c["components"]:
                        note = f"  · _{comp['note']}_" if comp.get("note") else ""
                        tag = "🟢" if comp["source"] == "kangxi" else "⚪"
                        st.markdown(f"- {tag} **{comp['component']}** "
                                    f"({comp['pinyin']}) = {comp['meaning']}{note}")

                if c["appears_in"]:
                    st.markdown("**Also appears in:**")
                    for ex in c["appears_in"]:
                        st.markdown(f"- **{ex['word']}** ({ex['pinyin']}) — {ex['meaning'][:60]}")
        st.divider()

st.caption("Data: CC-CEDICT + cjkvi-ids (via hanzipy) · Kangxi 214-radical dictionary. Runs 100% offline.")

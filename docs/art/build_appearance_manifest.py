#!/usr/bin/env python3
"""Rebuild only the 48-person review manifest; never changes CSV or Markdown.

Run python docs/art/build_appearance_manifest.py --check to verify the committed
sample without changing any file. Omit --check to regenerate it, or use --output
for a separate experiment. This is a document proof generator, not game code.
"""
from pathlib import Path
import argparse,json,random,hashlib,collections

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='重建／驗證45員工＋3招募候選的持久分層外觀資料樣本。')
parser.add_argument('--seed',type=int,default=20261023)
parser.add_argument('--output',type=Path,default=HERE/'appearance_manifest.json')
parser.add_argument('--check',action='store_true',help='只比對現有檔案，不寫入')
args=parser.parse_args()
output=args.output.resolve()
labels={
'body_type':['纖長窄肩','高挑寬肩','標準直身','短身窄肩','短身圓肩','厚實方肩','圓身落肩','修長方肩'],
'face_shape':['長方臉','短方臉','寬圓臉','窄橢圓臉','心型臉','菱形臉','長橢圓臉','短圓臉','梯形下顎','寬顴骨','窄下巴','飽滿頰'],
'hair_family':['俐落短髮','側分短髮','尖束短髮','側削短髮','直短鮑伯','高盤髮髻','側馬尾','短捲髮','蓬鬆捲髮','波浪鮑伯','長瀏海','中分短髮','寸頭','上梳短髮','精靈短髮','側辮','長雙束髮','光頭','側分長髮','平瀏海'],
'eye_shape':['細長眼','圓眼','上挑眼','平直眼','下垂眼','窄眼褶','深眼褶','寬眼距','近眼距','柔弧眼'],
'brow_shape':['平眉','劍眉','彎眉','濃短眉','細長眉','八字眉','高眉峰','柔圓眉'],
'nose_shape':['短圓鼻','長直鼻','寬鼻翼','小尖鼻','鈍鼻頭','窄鼻樑'],
'mouth_shape':['平直薄唇','圓弧唇','寬嘴','小嘴','厚下唇','明顯唇峰','短嘴角','長嘴角'],
'garment_structure':['翻領西裝領帶','開襟外套','背心襯衫','工作襯衫','合身西裝','立領外套','套頭針織','寬翻領西裝','長版外套','拉鍊外套'],
'glasses':['細圓框','方框','半框','粗圓框','窄長框','眉框'],
'facial_hair':['小鬍子','短山羊鬍','下巴鬍','短落腮鬍','濃鬍鬚','鬢角'],
'accessory':['窄領帶','寬領帶','領巾','圓胸針','方胸針','耳釘','細項鍊','口袋巾'],
'shoe_type':['窄頭皮鞋','圓頭皮鞋','低筒便鞋','綁帶鞋','短靴'],
'ears':['小圓耳','長耳廓','寬耳廓','貼頭耳','外張耳','厚耳垂','薄耳垂','尖耳廓'],
}
prefix={'body_type':'body','face_shape':'face','hair_family':'hair','eye_shape':'eye','brow_shape':'brow','nose_shape':'nose','mouth_shape':'mouth','garment_structure':'garment','glasses':'glasses','facial_hair':'beard','accessory':'accessory','ears':'ear','shoe_type':'shoe'}
definitions={k:[{'id':f'{prefix[k]}_{i+1:02d}','label':v} for i,v in enumerate(vals)] for k,vals in labels.items()}
for key,pre,vals in [
('skin_palette','skin',['#F0C8A5','#DCAD83','#C99064','#B17751','#945F42','#73482F']),
('hair_palette','hair_color',['#171D22','#2C2524','#49342A','#684938','#7B6C5E','#8D8A80','#B9B6AA','#D8D6C9']),
('garment_palette','garment_color',['#17323D','#287F7C','#5C6669','#594452','#936549','#59644F'])]:
    definitions[key]=[{'id':f'{pre}_{i+1:02d}','label':f'{pre}配色{i+1:02d}','hex':v} for i,v in enumerate(vals)]
back_map=[1,2,3,1,5,9,7,4,6,6,11,2,1,3,1,10,12,0,12,5]
for i,h in enumerate(definitions['hair_family']):
    h.update({'hair_front':f'hair_front_{i+1:02d}' if i!=17 else 'none','hair_back':f'hair_back_{back_map[i]:02d}' if back_map[i] else 'none'})
    h['allowed_fronts']=[h['hair_front']]
definitions['hair_family'][2]['allowed_fronts'].append('hair_front_18')
front_labels=[h['label']+'前髮' for h in definitions['hair_family']]
front_labels[17]='尖束短髮・額前碎瀏海變體'
definitions['hair_front']=[{'id':f'hair_front_{i+1:02d}','label':label} for i,label in enumerate(front_labels)]
definitions['hair_back']=[{'id':f'hair_back_{i+1:02d}','label':label} for i,label in enumerate(['貼頸短髮','短髮後腦','波浪短髮後腦','短捲後腦','直鮑伯後髮','波浪鮑伯後髮','低馬尾','高馬尾','盤髮髻','側辮後髮','及肩後髮','長後髮'])]
body_garments={f'body_{i+1:02d}':[f'garment_{(i+j)%10+1:02d}' for j in range(6)] for i in range(8)}
seed=args.seed
rng=random.Random(seed)
def balanced(values,n=48):
    items=(values*((n+len(values)-1)//len(values)))[:n];rng.shuffle(items);return items
for generation_attempt in range(512):
    pool={k:balanced([x['id'] for x in definitions[k]]) for k in ['body_type','face_shape','hair_family','eye_shape','brow_shape','nose_shape','mouth_shape']}
    garment_usage=collections.Counter();profiles=[]
    face_hair=set();body_hair=set()
    structural_fields=['body_type','face_shape','hair_family','eye_shape','brow_shape','nose_shape','mouth_shape','garment_structure']
    for i in range(48):
        # Search remaining balanced assignments without relaxing perceptual uniqueness.
        candidates=[]
        for j in range(i,48):
            for k in range(i,48):
                b=pool['body_type'][i];face=pool['face_shape'][j];hair=pool['hair_family'][k]
                if (face,hair) in face_hair or (b,hair) in body_hair:continue
                garments=sorted(body_garments[b],key=lambda g:(garment_usage[g],g))
                for g in garments:
                    if garment_usage[g]>=6:continue
                    a={key:pool[key][i] for key in pool};a.update(face_shape=face,hair_family=hair,garment_structure=g)
                    if all(sum(a[f]!=p['appearance'][f] for f in structural_fields)>=3 for p in profiles):
                        candidates.append((j,k,a));break
                if candidates:break
            if candidates:break
        if not candidates:break
        j,k,a=candidates[0]
        pool['face_shape'][i],pool['face_shape'][j]=pool['face_shape'][j],pool['face_shape'][i]
        pool['hair_family'][i],pool['hair_family'][k]=pool['hair_family'][k],pool['hair_family'][i]
        hair=next(h for h in definitions['hair_family'] if h['id']==a['hair_family'])
        a.update(hair_front=hair['allowed_fronts'][i%len(hair['allowed_fronts'])],hair_back=hair['hair_back'])
        for key in ['skin_palette','hair_palette','garment_palette','ears']:
            a[key]=definitions[key][rng.randrange(len(definitions[key]))]['id']
        for key,chance in [('glasses',.45),('facial_hair',.25),('accessory',.70)]:
            a[key]=rng.choice(definitions[key])['id'] if rng.random()<chance else 'none'
        a['shoe_type']=definitions['shoe_type'][i%5]['id']
        a['expression']='neutral'
        cid=f'EMP-{i+1:03d}' if i<45 else f'REC-{i-44:03d}'
        structural='|'.join(a[f] for f in structural_fields)
        appearance_hash=hashlib.sha256(json.dumps({k:v for k,v in a.items() if k!='expression'},sort_keys=True).encode()).hexdigest()
        profiles.append({'character_id':cid,'group':'active_staff' if i<45 else 'recruit_candidates','display_name':f'員工{i+1:02d}' if i<45 else f'候選人{i-44:02d}','appearance_profile_id':'AP-'+cid,'generation_nonce':i+1,'recruit_batch_id':f'review-batch-{seed}-001' if i>=45 else None,'appearance':a,'structural_signature':structural,'appearance_hash':appearance_hash})
        face_hair.add((a['face_shape'],a['hair_family']));body_hair.add((a['body_type'],a['hair_family']));garment_usage[a['garment_structure']]+=1
    if len(profiles)==48:break
else:raise AssertionError("Balanced structural pool exhausted after 512 deterministic attempts; expand artwork")
assert len(profiles)==48 and len(face_hair)==48 and len(body_hair)==48
assert len({p['appearance']['face_shape'] for p in profiles})==12
assert len({p['appearance']['hair_family'] for p in profiles})==20
for key,limit in [('body_type',6),('face_shape',4),('hair_family',3),('garment_structure',6)]:
    assert max(collections.Counter(p['appearance'][key] for p in profiles).values())<=limit,(key,limit)
manifest={'visual_style_source':'visual_style.json','schema_version':2,'purpose':'外觀規格與資料唯一性驗證；不是已實作的遊戲生成器或正式美術','seed':seed,'registry_id':f'appearance-review-{seed}','definitions':definitions,'compatibility':{'body_garments':body_garments,'hair_front_back':'由hair_family定義配對，禁止任意笛卡兒拼接'},'composition_order':{'sprite':['hair_back','shoe_type','body_type','garment_structure','face_shape','expression','facial_hair','glasses','hair_front','accessory'],'portrait':['hair_back','body_type','garment_structure','ears','face_shape','nose_shape','eye_shape','brow_shape','mouth_shape','facial_hair','glasses','hair_front','accessory']},'uniqueness':{'pool':'45在職＋3當批候選，共48名','structural_fields':structural_fields,'excludes':['姓名','衣色','髮色','膚色','職級','性別標籤'],'unique_face_hair':True,'unique_body_hair':True,'minimum_structural_hamming_distance':3,'max_counts':{'body_type':6,'face_shape':4,'hair_family':3,'garment_structure':6},'scope':'資料結構驗證已完成；實際合成畫面仍需灰階／縮圖人工檢查，不能以hash不重複宣稱美術已通過'},'persistence':{'save_fields':['character_id','appearance_profile_id','schema_version','appearance','appearance_hash','registry_id','generator_rng_state','recruit_batch_id'],'generation':'角色首次建立時固定；切頁、並排、存讀檔不重新抽取；更換表情不改身份','exhaustion':'不滿足配對／多樣性門檻時重抽資料；資產池不足則停止產生並擴充，禁止默默退回撞臉'},'profiles':profiles}
rendered=json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'
if args.check:
    if output.read_text()!=rendered:raise SystemExit('FAIL: 現有manifest與seed重建內容不同；請先檢查差異。')
    print('PASS: appearance_manifest.json逐byte可由seed重建；48人結構與相容性驗證通過。')
else:
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(rendered)
    print(output)
print('SHA256 '+hashlib.sha256(rendered.encode()).hexdigest())

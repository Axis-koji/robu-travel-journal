(function(){
  'use strict';

  function escapeHtml(value){
    return String(value).replace(/[&<>"']/g,function(character){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character];
    });
  }

  function addStylesheet(){
    if(document.querySelector('link[data-contact-feedback-style]')) return;
    var link=document.createElement('link');
    link.rel='stylesheet';
    link.href='/assets/css/contact-feedback.css';
    link.dataset.contactFeedbackStyle='';
    document.head.appendChild(link);
  }

  function template(articleTitle){
    return '<section class="contact-feedback" id="contact" aria-labelledby="contact-heading">'+
      '<details class="contact-details"><summary><span class="contact-icon" aria-hidden="true">✉</span><span><strong id="contact-heading">問い合わせ・ご感想</strong><small>記事へのご感想やご質問をお寄せください</small></span><span class="summary-action" aria-hidden="true">入力欄を開く</span></summary>'+
      '<div class="contact-panel"><p class="contact-intro">内容を確認したうえで、必要に応じてメールでお返事します。<span class="required-note">「必須」</span>の項目は必ずご入力ください。</p>'+
      '<form class="contact-form" novalidate><div class="contact-field-row contact-two-columns">'+
      '<label class="contact-field"><span>お名前 <em>必須</em></span><input type="text" name="name" autocomplete="name" maxlength="100" required placeholder="例：山田 太郎"><small class="contact-error" data-error-for="name"></small></label>'+
      '<label class="contact-field"><span>折り返し用メールアドレス <em>必須</em></span><input type="email" name="email" autocomplete="email" maxlength="254" required placeholder="例：name@example.com"><small class="contact-error" data-error-for="email"></small></label></div>'+
      '<div class="contact-field-row contact-two-columns"><label class="contact-field"><span>お電話番号 <i>任意</i></span><input type="tel" name="phone" autocomplete="tel" maxlength="30" inputmode="tel" placeholder="例：090-1234-5678"></label><label class="contact-field"><span>ご住所 <i>任意</i></span><input type="text" name="address" autocomplete="street-address" maxlength="300" placeholder="返信に必要な場合のみ"></label></div>'+
      '<label class="contact-field"><span>お問い合わせの種類 <em>必須</em></span><select name="category" required><option value="">選択してください</option><option>記事へのご感想</option><option>記事内容についてのご質問</option><option>掲載内容の訂正依頼</option><option>その他のお問い合わせ</option></select><small class="contact-error" data-error-for="category"></small></label>'+
      '<label class="contact-field"><span>内容 <em>必須</em></span><textarea name="message" rows="7" maxlength="3000" required placeholder="ご感想・お問い合わせ内容をご記入ください"></textarea><small class="contact-counter"><span data-message-count>0</span> / 3000文字</small><small class="contact-error" data-error-for="message"></small></label>'+
      '<label class="contact-consent"><input type="checkbox" name="consent" required><span><a href="/privacy-policy/">個人情報の取扱い</a>を確認し、問い合わせ対応のために入力情報を利用することに同意します。 <em>必須</em></span></label><small class="contact-error contact-consent-error" data-error-for="consent"></small>'+
      '<label class="contact-honeypot" aria-hidden="true">会社名<input type="text" name="company" tabindex="-1" autocomplete="off"></label><input type="hidden" name="source" value="'+escapeHtml(articleTitle)+'">'+
      '<div class="contact-security-note"><span aria-hidden="true">●</span><p><strong>入力内容はこのサイトに保存しません</strong><br>送信ボタンを押すと、ご利用端末のメールアプリが開きます。内容を確認して、メールアプリ側の送信ボタンを押してください。</p></div>'+
      '<button class="contact-submit" type="submit">メールアプリで送信内容を確認する</button><p class="contact-status" role="status" aria-live="polite"></p></form>'+
      '<aside class="contact-privacy"><h3>個人情報の取扱い</h3><p>氏名とメールアドレスは返信のために必須です。電話番号と住所は任意です。入力内容はWebサイト内には保存されず、訪問者が利用するメールアプリへ引き渡されます。</p></aside></div></details></section>';
  }

  function setError(form,name,text){
    var input=form.elements[name];
    var error=form.querySelector('[data-error-for="'+name+'"]');
    if(input&&input.classList) input.classList.toggle('contact-invalid',Boolean(text));
    if(error) error.textContent=text;
  }

  function bindForm(section){
    var form=section.querySelector('.contact-form');
    var message=form.elements.message;
    var count=form.querySelector('[data-message-count]');
    var status=form.querySelector('.contact-status');
    message.addEventListener('input',function(){count.textContent=String(message.value.length);});
    form.addEventListener('input',function(event){if(event.target.name)setError(form,event.target.name,'');status.textContent='';status.className='contact-status';});
    form.addEventListener('submit',function(event){
      event.preventDefault();
      var data=new FormData(form);var values=Object.fromEntries(data.entries());
      var rules={name:values.name&&values.name.trim()?'':'お名前を入力してください。',email:/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email||'')?'':'有効なメールアドレスを入力してください。',category:values.category?'':'種類を選択してください。',message:values.message&&values.message.trim()?'':'内容を入力してください。',consent:form.elements.consent.checked?'':'個人情報の取扱いへの同意が必要です。'};
      Object.keys(rules).forEach(function(name){setError(form,name,rules[name]);});
      if(Object.values(rules).some(Boolean)){status.textContent='入力内容をご確認ください。';status.className='contact-status contact-failure';var invalid=form.querySelector('.contact-invalid');if(invalid)invalid.focus();return;}
      if(values.company){status.textContent='送信を受け付けられませんでした。';status.className='contact-status contact-failure';return;}
      var source=values.source||document.title;
      var subject='【ろぶーの気になる事】'+values.category+'｜'+source;
      var body=['お名前：'+values.name,'折り返し用メールアドレス：'+values.email,'電話番号：'+(values.phone||'未記入'),'住所：'+(values.address||'未記入'),'お問い合わせの種類：'+values.category,'対象ページ：'+source,'ページURL：'+window.location.href,'','内容：',values.message].join('\r\n');
      var recipient=['koji','axis-jp.net'].join('@');
      status.textContent='メールアプリを開きます。内容を確認して送信してください。';status.className='contact-status contact-success';
      window.location.href='mailto:'+recipient+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    });
  }

  function init(){
    if(document.querySelector('.contact-feedback')) return;
    addStylesheet();
    var titleNode=document.querySelector('h1');
    var articleTitle=titleNode?titleNode.textContent.trim():document.title;
    var host=document.querySelector('[data-contact-page]')||document.querySelector('article')||document.querySelector('main');
    if(!host) return;
    host.insertAdjacentHTML('beforeend',template(articleTitle));
    var section=host.querySelector('.contact-feedback');
    if(host.hasAttribute('data-contact-page')) section.querySelector('details').open=true;
    bindForm(section);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

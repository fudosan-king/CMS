import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'switch': {
                name : translator.t('Wc switch'),
                uri: require('./wc.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#fbfafa'
            }   
        };
    },
};
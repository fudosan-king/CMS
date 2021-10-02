import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'tame_lightOak': {
                name : translator.t('Light oak'),
                uri: require('./light-oak.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#D1B8A4'
            }   
        };
    },
};
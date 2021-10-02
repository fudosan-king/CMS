import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'chair_skin': {
                name : translator.t('Cushion'),
                uri: require('./black.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#1C1C1C'
            }   
        };
    },
};
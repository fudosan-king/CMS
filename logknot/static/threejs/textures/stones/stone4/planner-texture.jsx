import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'stone_4': {
                name : translator.t('Stone') + '4',
                uri: require('./graniite.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F8FCF8'
            }   
        };
    },
};
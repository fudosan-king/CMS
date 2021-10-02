import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'stone_2': {
                name : translator.t('Stone' + '2'),
                uri: require('./stone_2.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#d7a161'
            }   
        };
    },
};
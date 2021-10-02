import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'stone_sliver': {
                name : translator.t('Silver'),
                uri: require('./sliver-stone.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E6E3DF'
            }   
        };
    },
};
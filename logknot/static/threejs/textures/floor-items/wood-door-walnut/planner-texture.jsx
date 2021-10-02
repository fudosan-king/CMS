import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_door_walnut': {
                name : translator.t('Wood Door Walnut'),
                uri: require('./go-wanut.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#371D01',
                hidden: true,
            }   
        };
    },
};
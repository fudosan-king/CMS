import React from 'react';
export const getBase64Code=()=>{
   return (
        'data:image/jpeg;base64,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'
   );
   }
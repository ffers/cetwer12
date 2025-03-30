function deleteBlock(id){
    let oldBlock = id.closest(".row");
    oldBlock.parentNode.removeChild(oldBlock);
}
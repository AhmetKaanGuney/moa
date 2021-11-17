var init_happened = false




updateUserGroupSelect()
// check if default initialization happend
// if not trigger these events
if (!init_happened) {
    sourceGroupSelect.onchange()
    init_happened = true
}

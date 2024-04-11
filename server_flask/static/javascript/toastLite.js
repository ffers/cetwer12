const trigerToastLite = document.getElementById('trigerToastLite')
const toastLite = document.getElementById('toastLite')

if (trigerToastLite) {
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLite)
trigerToastLite.addEventListener('click', () => {
toastBootstrap.show()
})
}
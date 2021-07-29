module.exports = async function (_promise) {
  return new Promise((resolve, reject) => {
    _promise
      .then(f => {
        resolve([null, f])
      })
      .catch(e => {
        resolve([e, null])
      })
  })
}

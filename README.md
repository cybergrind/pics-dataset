# pics-dataset
Tag and manage dataset of pictures



## Development

```bash
# add migration
make generate-migration MESSAGE="migration message"
```

```svelte
<Cropper {image} bind:crop bind:zoom minZoom={0} restrictPosition={false} />
```


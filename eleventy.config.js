import { readFile } from "node:fs/promises";

export default function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy("src/**/*.css");

    // Every album must have a Discogs link; Bandcamp is optional.
    eleventyConfig.on("eleventy.before", async () => {
        const albums = JSON.parse(await readFile("src/_data/albums.json", "utf8"));
        const missing = albums.filter((album) => !album.discogs);
        if (missing.length) {
            throw new Error(
                `Albums missing a Discogs link: ${missing.map((a) => `${a.artist} - ${a.title}`).join(", ")}`,
            );
        }
    });

    // Groups albums into decades (newest first), each sorted by year
    // descending, then artist and title ascending.
    eleventyConfig.addFilter("byDecade", (albums) => {
        const compare = (a, b) =>
            b.year - a.year ||
            a.artist.localeCompare(b.artist, "en", { sensitivity: "base" }) ||
            a.title.localeCompare(b.title, "en", { sensitivity: "base" });
        const decades = new Map();
        for (const album of [...albums].sort(compare)) {
            const decade = Math.floor(album.year / 10) * 10;
            if (!decades.has(decade)) decades.set(decade, []);
            decades.get(decade).push(album);
        }
        return [...decades].map(([decade, albums]) => ({ decade, albums }));
    });

    return {
        dir: {
            input: "src",
            output: "_site",
        },
    };
}

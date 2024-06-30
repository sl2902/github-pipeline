

with 
parsed_data as (
    select 
        id,
        json_parse(response) as parsed_response
    from {{ ref('stg_raw_issues') }}
),
labels_extracted as (
    select
        id,
        cast(json_extract(parsed_response, '$.labels') as array(json)) AS labels_json
    from parsed_data
),
flattened as (
    select
        id,
        label AS label,
        json_extract(label, '$.name') as name,
        json_extract(label, '$.color') as color,
        json_extract(label, '$.description') as description
    from labels_extracted,
    unnest(labels_json) as t(label)
),
    top_3 as (
    select
        repo,
        name,
        count(*) as num_labels,
        dense_rank() over(partition by repo order by count(*) desc) as rn_top_3
    from
        flattened a join {{ ref('stg_issues') }} b on a.id = b.id
    group by
        repo,
        name
)
select
	repo,
	replace(cast(name as varchar), '"') as label,
	num_labels
from
 	top_3
where 
	rn_top_3 < 4
order by
	repo,
	num_labels desc
